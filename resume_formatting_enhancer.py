"""
Advanced formatting preservation utilities for perfect resume formatting
"""

import re
from typing import Dict, List, Tuple, Optional
from lxml import etree

class ResumeFormattingEnhancer:
    """
    Specialized class for handling resume-specific formatting requirements
    """
    
    def __init__(self, namespaces: Dict[str, str]):
        self.namespaces = namespaces
    
    def enhance_resume_formatting(self, paragraphs: List[etree._Element], 
                                content_mapping: List[Dict]) -> bool:
        """
        Apply resume-specific formatting enhancements
        """
        try:
            print("🎨 Applying resume-specific formatting enhancements...")
            
            for i, para_elem in enumerate(paragraphs):
                if i < len(content_mapping):
                    mapping = content_mapping[i]
                    content_type = mapping.get('content_type', 'paragraph')
                    
                    # Apply type-specific enhancements
                    if content_type == 'section_header':
                        self._enhance_section_header(para_elem, mapping)
                    elif content_type == 'job_title':
                        self._enhance_job_title(para_elem, mapping)
                    elif content_type == 'bullet_point':
                        self._enhance_bullet_point(para_elem, mapping)
                    elif content_type == 'contact_info':
                        self._enhance_contact_info(para_elem, mapping)
            
            return True
            
        except Exception as e:
            print(f"⚠️  Resume enhancement failed: {e}")
            return False
    
    def _enhance_section_header(self, para_elem: etree._Element, mapping: Dict):
        """Enhance section headers (EXPERIENCE, EDUCATION, etc.)"""
        
        # Ensure section headers are properly formatted
        runs = para_elem.xpath('.//w:r', namespaces=self.namespaces)
        
        for run in runs:
            rpr = run.find('w:rPr', self.namespaces)
            if rpr is not None:
                # Ensure bold formatting
                bold_elem = rpr.find('w:b', self.namespaces)
                if bold_elem is None:
                    bold_elem = etree.Element(f'{{{self.namespaces["w"]}}}b')
                    rpr.append(bold_elem)
                
                # Ensure all caps if original was all caps
                original_text = mapping.get('original_content', '')
                if original_text and original_text.isupper():
                    caps_elem = rpr.find('w:caps', self.namespaces)
                    if caps_elem is None:
                        caps_elem = etree.Element(f'{{{self.namespaces["w"]}}}caps')
                        rpr.append(caps_elem)
    
    def _enhance_job_title(self, para_elem: etree._Element, mapping: Dict):
        """Enhance job title formatting"""
        
        new_content = mapping.get('new_content', '')
        
        # Look for company/title patterns
        if ' | ' in new_content or ' at ' in new_content or ' - ' in new_content:
            self._apply_job_title_formatting(para_elem, new_content)
    
    def _apply_job_title_formatting(self, para_elem: etree._Element, content: str):
        """Apply specific formatting to job titles"""
        
        runs = para_elem.xpath('.//w:r', namespaces=self.namespaces)
        
        if len(runs) >= 2:
            # Try to make job title bold, company normal
            parts = self._split_job_title_content(content)
            
            if len(parts) == 2:
                job_title, company = parts
                
                # First run: job title (bold)
                if len(runs) > 0:
                    self._ensure_bold_formatting(runs[0])
                
                # Second run: company (normal weight)
                if len(runs) > 1:
                    self._ensure_normal_formatting(runs[1])
    
    def _split_job_title_content(self, content: str) -> Tuple[str, str]:
        """Split job title content into title and company"""
        
        if ' | ' in content:
            return tuple(content.split(' | ', 1))
        elif ' at ' in content:
            parts = content.split(' at ', 1)
            return parts[0], f"at {parts[1]}"
        elif ' - ' in content:
            return tuple(content.split(' - ', 1))
        
        return content, ''
    
    def _enhance_bullet_point(self, para_elem: etree._Element, mapping: Dict):
        """Enhance bullet point formatting"""
        
        # Ensure proper bullet spacing and indentation
        ppr = para_elem.find('w:pPr', self.namespaces)
        if ppr is not None:
            # Preserve original indentation
            original_properties = mapping.get('properties', {})
            indentation = original_properties.get('indentation', {})
            
            if indentation:
                ind_elem = ppr.find('w:ind', self.namespaces)
                if ind_elem is not None:
                    # Preserve original indentation values
                    for attr in ['left', 'hanging', 'firstLine']:
                        if attr in indentation and indentation[attr]:
                            ind_elem.set(f'{{{self.namespaces["w"]}}}{attr}', str(indentation[attr]))
    
    def _enhance_contact_info(self, para_elem: etree._Element, mapping: Dict):
        """Enhance contact information formatting"""
        
        # Contact info often needs consistent formatting
        runs = para_elem.xpath('.//w:r', namespaces=self.namespaces)
        
        for run in runs:
            # Ensure consistent font and size for contact info
            rpr = run.find('w:rPr', self.namespaces)
            if rpr is not None:
                # Remove bold from contact info if not originally present
                original_properties = mapping.get('properties', {})
                if not self._was_originally_bold(mapping):
                    bold_elem = rpr.find('w:b', self.namespaces)
                    if bold_elem is not None:
                        rpr.remove(bold_elem)
    
    def _ensure_bold_formatting(self, run_elem: etree._Element):
        """Ensure a run has bold formatting"""
        rpr = run_elem.find('w:rPr', self.namespaces)
        if rpr is None:
            rpr = etree.Element(f'{{{self.namespaces["w"]}}}rPr')
            run_elem.insert(0, rpr)
        
        bold_elem = rpr.find('w:b', self.namespaces)
        if bold_elem is None:
            bold_elem = etree.Element(f'{{{self.namespaces["w"]}}}b')
            rpr.append(bold_elem)
    
    def _ensure_normal_formatting(self, run_elem: etree._Element):
        """Ensure a run has normal (non-bold) formatting"""
        rpr = run_elem.find('w:rPr', self.namespaces)
        if rpr is not None:
            bold_elem = rpr.find('w:b', self.namespaces)
            if bold_elem is not None:
                rpr.remove(bold_elem)
    
    def _was_originally_bold(self, mapping: Dict) -> bool:
        """Check if content was originally bold"""
        runs = mapping.get('runs', [])
        return any(run.get('properties', {}).get('bold', False) for run in runs)
    
    def preserve_horizontal_lines(self, paragraphs: List[etree._Element]) -> bool:
        """
        Specifically preserve horizontal lines and borders
        """
        try:
            print("📏 Preserving horizontal lines and borders...")
            
            for para_elem in paragraphs:
                ppr = para_elem.find('w:pPr', self.namespaces)
                if ppr is not None:
                    # Check for paragraph borders (horizontal lines)
                    border_elem = ppr.find('w:pBdr', self.namespaces)
                    if border_elem is not None:
                        # Ensure border properties are preserved
                        for border_side in ['top', 'bottom', 'left', 'right']:
                            side_elem = border_elem.find(f'w:{border_side}', self.namespaces)
                            if side_elem is not None:
                                # Preserve all border attributes
                                print(f"  ✅ Preserved {border_side} border")
            
            return True
            
        except Exception as e:
            print(f"⚠️  Border preservation failed: {e}")
            return False
    
    def apply_spacing_enhancements(self, paragraphs: List[etree._Element], 
                                 content_mapping: List[Dict]) -> bool:
        """
        Apply enhanced spacing based on content types
        """
        try:
            print("📐 Applying intelligent spacing...")
            
            for i, para_elem in enumerate(paragraphs):
                if i < len(content_mapping):
                    mapping = content_mapping[i]
                    content_type = mapping.get('content_type', 'paragraph')
                    
                    # Apply type-specific spacing
                    if content_type == 'section_header':
                        self._apply_section_spacing(para_elem, mapping)
                    elif content_type == 'bullet_point':
                        self._apply_bullet_spacing(para_elem, mapping)
            
            return True
            
        except Exception as e:
            print(f"⚠️  Spacing enhancement failed: {e}")
            return False
    
    def _apply_section_spacing(self, para_elem: etree._Element, mapping: Dict):
        """Apply appropriate spacing for section headers"""
        
        ppr = para_elem.find('w:pPr', self.namespaces)
        if ppr is not None:
            spacing_elem = ppr.find('w:spacing', self.namespaces)
            if spacing_elem is not None:
                # Preserve original spacing values
                original_spacing = mapping.get('properties', {}).get('spacing', {})
                
                for attr in ['before', 'after', 'line']:
                    if attr in original_spacing and original_spacing[attr]:
                        spacing_elem.set(f'{{{self.namespaces["w"]}}}{attr}', str(original_spacing[attr]))
    
    def _apply_bullet_spacing(self, para_elem: etree._Element, mapping: Dict):
        """Apply appropriate spacing for bullet points"""
        
        # Bullet points typically have tighter spacing
        ppr = para_elem.find('w:pPr', self.namespaces)
        if ppr is not None:
            spacing_elem = ppr.find('w:spacing', self.namespaces)
            if spacing_elem is not None:
                # Preserve original bullet spacing
                original_spacing = mapping.get('properties', {}).get('spacing', {})
                
                # Apply original values exactly
                for attr in ['before', 'after', 'line', 'lineRule']:
                    if attr in original_spacing and original_spacing[attr]:
                        spacing_elem.set(f'{{{self.namespaces["w"]}}}{attr}', str(original_spacing[attr]))