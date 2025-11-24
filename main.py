"""
Optimized Anki flashcard generation with parallelization
Expected speedup: 10-20x faster (20 hours -> 1-2 hours)
"""
from text_speech import synthesize_speech
from gpt_to_ita import generate_phrase_and_translate
from word_reader import read_words_from_file
from anki_template import create_anki_model
from anki_paste import add_note, upload_audio_to_anki, create_deck
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.cloud import texttospeech
import google.generativeai as genai
import os
import json
from tqdm import tqdm
import time
import signal
import sys

# Configuration
CHECKPOINT_FILE = "progress_checkpoint.json"
CHECKPOINT_INTERVAL = 100  # Save progress every 100 words
MAX_WORKERS = 15  # Process 15 words concurrently (Tier 1: 250 RPM / 4 calls per word ≈ 60, reduced for safety)

def load_checkpoint():
    """Load progress from checkpoint file"""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {"completed_indices": [], "last_index": -1}

def save_checkpoint(checkpoint_data):
    """Save progress to checkpoint file"""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint_data, f)

def process_single_word(args):
    """Process a single word: generate content and create Anki card"""
    i, word, language, deck_name, model_name, gemini_model, tts_client = args
    
    try:
        # Generate phrase and translations (with 3/4 calls parallelized internally)
        word, generated_phrase, translated_word, translated_phrase, word_definition = \
            generate_phrase_and_translate(word, language, model=gemini_model)
        
        # Synthesize speech (reusing TTS client)
        word_audio = synthesize_speech(word, client=tts_client)
        phrase_audio = synthesize_speech(generated_phrase, client=tts_client)
        
        # Upload audio files to Anki's media library
        word_audio_file = upload_audio_to_anki(f"word_{i}.mp3", word_audio)
        phrase_audio_file = upload_audio_to_anki(f"phrase_{i}.mp3", phrase_audio)
        
        # Create Anki note fields
        fields = {
            "Native word": translated_word,
            "Native phrase": translated_phrase,
            "Foreign word": word,
            "Foreign word audio": f"[sound:{word_audio_file}]",
            "Foreign phrase": generated_phrase,
            "Foreign phrase audio": f"[sound:{phrase_audio_file}]",
            "Definition": word_definition
        }
        
        # Add note to Anki
        result = add_note(deck_name, model_name, fields)
        
        # Check for errors
        if result.get('error') is not None:
            return {"index": i, "word": word, "success": False, "error": str(result['error'])}
        
        return {"index": i, "word": word, "success": True, "error": None}
        
    except Exception as e:
        error_msg = str(e)
        # Check if it's a quota error
        is_quota_error = "quota" in error_msg.lower() or "429" in error_msg
        return {
            "index": i, 
            "word": word, 
            "success": False, 
            "error": error_msg,
            "quota_exceeded": is_quota_error
        }

def main():
    print("=" * 80)
    print("OPTIMIZED ANKI FLASHCARD GENERATION")
    print("=" * 80)
    
    # Set up graceful interrupt handler
    interrupted = {"value": False}
    completed_indices = set()
    
    def signal_handler(sig, frame):
        """Handle Ctrl+C gracefully"""
        if not interrupted["value"]:
            interrupted["value"] = True
            print("\n\n🛑 Manual stop requested (Ctrl+C detected)...")
            print("   Finishing current batch and saving checkpoint...")
            print("   Press Ctrl+C again to force quit (will lose progress)\n")
        else:
            print("\n❌ Force quit - progress since last checkpoint will be lost!")
            sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create Anki model and deck
    model_name = "your_model_name"
    deck_name = "your_deck_name"
    print("\n📋 Creating Anki model and deck...")
    create_anki_model(model_name)
    create_deck(deck_name)
    
    # Read words from file
    file_path = r"C:\Users\titot\Desktop\PMW\Anki_Project\Anki_Improved\lemma 5000.txt"
    print(f"\n📖 Reading words from: {file_path}")
    words = read_words_from_file(file_path)
    print(f"   Total words: {len(words)}")
    
    # Set language
    language = "Italian"
    
    # Load checkpoint to resume if interrupted
    checkpoint = load_checkpoint()
    completed_indices.update(checkpoint["completed_indices"])
    
    # Get words already in Anki to avoid wasting API calls
    print("\n🔍 Checking existing cards in Anki...")
    from anki_paste import invoke
    result = invoke('findNotes', {'query': f'deck:"{deck_name}"'})
    existing_note_ids = result.get('result', [])
    
    if existing_note_ids:
        result = invoke('notesInfo', {'notes': existing_note_ids})
        notes = result.get('result', [])
        import re
        existing_words = set()
        for note in notes:
            fields = note.get('fields', {})
            foreign_word = fields.get('Foreign word', {}).get('value', '')
            if foreign_word:
                # Remove audio tags
                foreign_word = re.sub(r'\[sound:.*?\]', '', foreign_word).strip()
                existing_words.add(foreign_word)
        print(f"   Found {len(existing_words)} existing cards in Anki")
    else:
        existing_words = set()
        print(f"   No existing cards found")
    
    if completed_indices:
        print(f"\n🔄 Resuming from checkpoint: {len(completed_indices)} words already processed")
    
    # Filter out already completed words AND words already in Anki
    words_to_process = [
        (i, word) for i, word in enumerate(words) 
        if i not in completed_indices and word not in existing_words
    ]
    
    if not words_to_process:
        print("\n✅ All words already processed!")
        return
    
    print(f"   Words to process: {len(words_to_process)}")
    print(f"   (Skipping {len(words) - len(words_to_process)} already in Anki or checkpoint)")
    
    # Initialize shared resources (reuse across all words)
    print("\n🔧 Initializing API clients...")
    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
    tts_client = texttospeech.TextToSpeechClient()
    
    # Process words in parallel
    print(f"\n🚀 Processing {len(words_to_process)} words with {MAX_WORKERS} concurrent workers...")
    print("   (This will be significantly faster than the sequential version)\n")
    
    start_time = time.time()
    errors = []
    successful_count = 0
    quota_exceeded = False
    
    # Create argument tuples for parallel processing
    args_list = [
        (i, word, language, deck_name, model_name, gemini_model, tts_client)
        for i, word in words_to_process
    ]
    
    # Process with progress bar
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_single_word, args): args[0] for args in args_list}
        
        with tqdm(total=len(words_to_process), desc="Processing words", unit="word") as pbar:
            for future in as_completed(futures):
                result = future.result()
                
                if result["success"]:
                    successful_count += 1
                    completed_indices.add(result["index"])
                else:
                    errors.append(result)
                    print(f"\n⚠️  Error with word {result['index']} ({result['word']}): {result['error']}")
                    
                    # Check if quota exceeded
                    if result.get("quota_exceeded", False):
                        quota_exceeded = True
                
                # If quota exceeded or manually interrupted, stop submitting new work
                if quota_exceeded:
                    print("\n🛑 Quota limit detected - stopping gracefully...")
                    print("   Waiting for in-flight requests to complete...")
                    break
                
                if interrupted["value"]:
                    print("   Stopping after current batch completes...")
                    break
                
                pbar.update(1)
                
                # Save checkpoint periodically
                if len(completed_indices) % CHECKPOINT_INTERVAL == 0:
                    save_checkpoint({
                        "completed_indices": list(completed_indices),
                        "last_index": max(completed_indices)
                    })
    
    # Final checkpoint save
    save_checkpoint({
        "completed_indices": list(completed_indices),
        "last_index": max(completed_indices) if completed_indices else -1
    })
    
    # Print summary
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 80)
    
    if interrupted["value"]:
        print("MANUALLY STOPPED")
        print("=" * 80)
        print(f"✅ Successfully processed: {successful_count}/{len(words_to_process)} words before manual stop")
        print(f"💾 Progress saved to checkpoint file")
        print(f"⏱️  Total time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
        print(f"\n🔄 Run 'python.exe main.py' again to continue from where you left off")
    elif quota_exceeded:
        print("QUOTA LIMIT REACHED - GRACEFUL SHUTDOWN")
        print("=" * 80)
        print(f"✅ Successfully processed: {successful_count}/{len(words_to_process)} words before quota limit")
        print(f"💾 Progress saved to checkpoint file")
        print(f"⏱️  Total time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
        print(f"\n📅 Quota resets at midnight Pacific time")
        print(f"🔄 Run 'python.exe main.py' again tomorrow to continue from where you left off")
    else:
        print("PROCESSING COMPLETE")
        print("=" * 80)
        print(f"✅ Successfully processed: {successful_count}/{len(words_to_process)} words")
        print(f"❌ Errors: {len(errors)}")
        print(f"⏱️  Total time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
        print(f"📊 Average time per word: {elapsed_time/len(words_to_process):.2f} seconds")
    
    if errors and not quota_exceeded:
        print(f"\n⚠️  Errors occurred with {len(errors)} words:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"   - Word {error['index']} ({error['word']}): {error['error']}")
        if len(errors) > 10:
            print(f"   ... and {len(errors) - 10} more errors")
        
        print("\n💾 Progress saved to checkpoint file")
        print(f"   To retry failed words, just run this script again")

if __name__ == "__main__":
    main()
