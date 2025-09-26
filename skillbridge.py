import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import init, Fore, Style
from ai_provider import AIProvider
from document_processor import DocumentProcessor
from config import *

# Initialize colorama for cross-platform colored output
init()

class ResumeWatcher(FileSystemEventHandler):
    """Watches for JD.docx and CurrentResume.docx files and processes them"""
    
    def __init__(self, watch_folder: str):
        self.watch_folder = Path(watch_folder)
        self.ai_provider = AIProvider()
        self.processing = False
        
        # Ensure watch folder exists
        self.watch_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"{Fore.GREEN}📁 Watching folder: {self.watch_folder.absolute()}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{self.ai_provider.get_provider_info()}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🔍 Drop 'JD.docx' and 'CurrentResume.docx' files to start processing...{Style.RESET_ALL}")
    
    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return
        
        self.check_and_process()
    
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
        
        # Small delay to ensure file is fully written
        time.sleep(1)
        self.check_and_process()
    
    def check_and_process(self):
        """Check if both required files exist and process them"""
        if self.processing:
            return
        
        jd_file = self.watch_folder / "JD.docx"
        resume_file = self.watch_folder / "CurrentResume.docx"
        output_file = self.watch_folder / OUTPUT_FILENAME
        error_file = self.watch_folder / ERROR_FILENAME
        
        # Check if both files exist
        if jd_file.exists() and resume_file.exists():
            self.processing = True
            
            print(f"\n{Fore.GREEN}🚀 Both files detected! Starting resume tailoring...{Style.RESET_ALL}")
            
            try:
                # Extract text from documents
                print(f"{Fore.BLUE}📖 Reading job description...{Style.RESET_ALL}")
                jd_content = DocumentProcessor.extract_text_from_docx(str(jd_file))
                
                print(f"{Fore.BLUE}📄 Reading current resume...{Style.RESET_ALL}")
                resume_content = DocumentProcessor.extract_text_from_docx(str(resume_file))
                
                if not jd_content or not resume_content:
                    raise Exception("Could not extract text from one or both documents")
                
                # Generate tailored resume
                print(f"{Fore.BLUE}🤖 Tailoring resume with AI...{Style.RESET_ALL}")
                tailored_content = self.ai_provider.generate_response(jd_content, resume_content)
                
                if not tailored_content:
                    raise Exception("AI failed to generate tailored resume content")
                
                # Create the tailored resume document
                print(f"{Fore.BLUE}📝 Creating formatted resume...{Style.RESET_ALL}")
                success = DocumentProcessor.create_tailored_resume(
                    str(resume_file),
                    tailored_content,
                    str(output_file)
                )
                
                if success:
                    print(f"\n{Fore.GREEN}✅ SUCCESS! Tailored resume created: {OUTPUT_FILENAME}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}📁 Location: {output_file.absolute()}{Style.RESET_ALL}")
                    
                    # Clean up input files (optional)
                    # jd_file.unlink()
                    # resume_file.unlink()
                    
                else:
                    raise Exception("Failed to create tailored resume document")
                
            except Exception as e:
                print(f"\n{Fore.RED}❌ Error processing files: {e}{Style.RESET_ALL}")
                
                # Create error document
                DocumentProcessor.create_error_document(
                    str(e),
                    str(error_file)
                )
                print(f"{Fore.YELLOW}📄 Error details saved to: {ERROR_FILENAME}{Style.RESET_ALL}")
            
            finally:
                self.processing = False
                print(f"\n{Fore.YELLOW}🔍 Ready for next files...{Style.RESET_ALL}")

def main():
    """Main function to start the file watcher"""
    print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}🌉 SkillBridge - Automated Resume Tailoring{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    
    # Create watch folder
    watch_path = Path(WATCH_FOLDER).expanduser().absolute()
    
    # Setup file watcher
    event_handler = ResumeWatcher(str(watch_path))
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=False)
    
    # Check AI provider status
    if AI_PROVIDER.lower() == "ollama" and not event_handler.ai_provider.is_ollama_available():
        print(f"\n{Fore.RED}❌ Ollama is not running!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please install and start Ollama:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Download from: https://ollama.ai{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Install and run: ollama serve{Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. Then restart SkillBridge{Style.RESET_ALL}")
        return
    
    # Start watching
    observer.start()
    
    try:
        print(f"\n{Fore.CYAN}Instructions:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Save your job description as 'JD.docx'{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Save your current resume as 'CurrentResume.docx'{Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. Drop both files into: {watch_path}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}4. Wait for 'TailoredResume.docx' to appear!{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Press Ctrl+C to stop watching...{Style.RESET_ALL}\n")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Stopping SkillBridge...{Style.RESET_ALL}")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    main()