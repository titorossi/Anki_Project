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

# Configuration
CHECKPOINT_FILE = "progress_checkpoint.json"
CHECKPOINT_INTERVAL = 100  # Save progress every 100 words
MAX_WORKERS = 50  # Process 50 words concurrently (adjust based on rate limits)

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
        return {"index": i, "word": word, "success": False, "error": str(e)}

def main():
    print("=" * 80)
    print("OPTIMIZED ANKI FLASHCARD GENERATION")
    print("=" * 80)
    
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
    completed_indices = set(checkpoint["completed_indices"])
    
    if completed_indices:
        print(f"\n🔄 Resuming from checkpoint: {len(completed_indices)} words already processed")
    
    # Filter out already completed words
    words_to_process = [(i, word) for i, word in enumerate(words) if i not in completed_indices]
    
    if not words_to_process:
        print("\n✅ All words already processed!")
        return
    
    print(f"   Words remaining: {len(words_to_process)}")
    
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
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"✅ Successfully processed: {successful_count}/{len(words_to_process)} words")
    print(f"❌ Errors: {len(errors)}")
    print(f"⏱️  Total time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    print(f"📊 Average time per word: {elapsed_time/len(words_to_process):.2f} seconds")
    
    if errors:
        print(f"\n⚠️  Errors occurred with {len(errors)} words:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"   - Word {error['index']} ({error['word']}): {error['error']}")
        if len(errors) > 10:
            print(f"   ... and {len(errors) - 10} more errors")
    
    print("\n💾 Progress saved to checkpoint file")
    print(f"   To restart from checkpoint, just run this script again")

if __name__ == "__main__":
    main()
