import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from typing import Optional
import re

class DocumentProcessor:
    """Handles reading and writing Word documents while preserving formatting"""
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> Optional[str]:
        """Extract text content from a Word document"""
        try:
            doc = Document(file_path)
            full_text = []
            
            for paragraph in doc.paragraphs:
                full_text.append(paragraph.text)
            
            # Also extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        full_text.append(cell.text)
            
            return '\n'.join(full_text)
        except Exception as e:
            print(f"❌ Error reading document {file_path}: {e}")
            return None
    
    @staticmethod
    def create_tailored_resume(original_resume_path: str, tailored_content: str, output_path: str) -> bool:
        """Create a new resume with tailored content while preserving original formatting"""
        try:
            # Load the original document to preserve formatting
            original_doc = Document(original_resume_path)
            
            # Create a new document based on the original
            new_doc = Document()
            
            # Copy styles from original document
            DocumentProcessor._copy_styles(original_doc, new_doc)
            
            # Process the tailored content and apply formatting
            DocumentProcessor._apply_formatted_content(new_doc, tailored_content, original_doc)
            
            # Save the new document
            new_doc.save(output_path)
            return True
            
        except Exception as e:
            print(f"❌ Error creating tailored resume: {e}")
            return False
    
    @staticmethod
    def create_error_document(error_message: str, output_path: str) -> bool:
        """Create an error document with the error message"""
        try:
            doc = Document()
            
            # Add title
            title = doc.add_heading('SkillBridge Processing Error', 0)
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Add error message
            doc.add_paragraph()
            error_para = doc.add_paragraph('We apologize, but there was an error processing your resume:')
            error_para.runs[0].bold = True
            
            doc.add_paragraph()
            doc.add_paragraph(error_message)
            
            doc.add_paragraph()
            doc.add_paragraph('Please check:')
            
            checklist = [
                '• Both JD.docx and CurrentResume.docx files are valid Word documents',
                '• The files contain readable text content',
                '• Your internet connection (if using OpenAI)',
                '• Ollama is running (if using local AI)',
                '• Try again in a few moments'
            ]
            
            for item in checklist:
                doc.add_paragraph(item)
            
            doc.add_paragraph()
            footer = doc.add_paragraph('If the problem persists, please check the console for detailed error messages.')
            footer.runs[0].italic = True
            
            doc.save(output_path)
            return True
            
        except Exception as e:
            print(f"❌ Error creating error document: {e}")
            return False
    
    @staticmethod
    def _copy_styles(source_doc: Document, target_doc: Document):
        """Copy styles from source document to target document"""
        try:
            # This is a simplified version - python-docx has limitations
            # but we'll do our best to preserve basic formatting
            pass
        except:
            pass
    
    @staticmethod
    def _apply_formatted_content(doc: Document, content: str, original_doc: Document):
        """Apply the tailored content to the document with formatting"""
        
        # Split content into paragraphs
        paragraphs = content.split('\n')
        
        for para_text in paragraphs:
            para_text = para_text.strip()
            if not para_text:
                continue
            
            # Determine paragraph type and apply appropriate formatting
            if DocumentProcessor._is_heading(para_text):
                heading = doc.add_heading(para_text, level=1)
                heading.runs[0].font.size = Pt(14)
                heading.runs[0].bold = True
            
            elif DocumentProcessor._is_subheading(para_text):
                subheading = doc.add_heading(para_text, level=2)
                subheading.runs[0].font.size = Pt(12)
                subheading.runs[0].bold = True
            
            elif DocumentProcessor._is_bullet_point(para_text):
                bullet_para = doc.add_paragraph(para_text, style='List Bullet')
            
            else:
                # Regular paragraph
                regular_para = doc.add_paragraph(para_text)
                
                # Apply bold formatting to what looks like job titles or company names
                DocumentProcessor._apply_smart_formatting(regular_para)
    
    @staticmethod
    def _is_heading(text: str) -> bool:
        """Determine if text should be formatted as a main heading"""
        headings = [
            'professional summary', 'summary', 'objective', 'profile',
            'work experience', 'experience', 'employment history',
            'education', 'skills', 'technical skills', 'core competencies',
            'certifications', 'awards', 'projects', 'achievements'
        ]
        return any(heading in text.lower() for heading in headings) and len(text) < 50
    
    @staticmethod
    def _is_subheading(text: str) -> bool:
        """Determine if text should be formatted as a subheading (job title/company)"""
        # Look for patterns like "Job Title | Company Name" or "Company Name - Job Title"
        patterns = [
            r'.*\|.*',  # Contains pipe
            r'.*-.*',   # Contains dash
            r'.*at .*', # Contains "at"
        ]
        return any(re.match(pattern, text) for pattern in patterns) and len(text) < 100
    
    @staticmethod
    def _is_bullet_point(text: str) -> bool:
        """Determine if text should be formatted as a bullet point"""
        return text.startswith('•') or text.startswith('-') or text.startswith('*')
    
    @staticmethod
    def _apply_smart_formatting(paragraph):
        """Apply smart formatting to paragraph text"""
        text = paragraph.text
        
        # Make job titles and company names bold (simplified approach)
        # This is a basic implementation - could be enhanced
        if '|' in text or ' - ' in text or ' at ' in text:
            # Likely a job title/company line
            paragraph.runs[0].bold = True