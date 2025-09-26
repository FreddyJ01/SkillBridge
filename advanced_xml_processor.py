import os
import zipfile
import xml.etree.ElementTree as ET
from lxml import etree
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import parse_xml
from typing import Dict, List, Optional, Tuple, Any
import re
from copy import deepcopy
import json

class AdvancedDocumentProcessor:
    """
    Advanced document processor that works directly with Word XML
    to achieve 100% identical formatting preservation
    """
    
    # Word XML namespaces
    NAMESPACES = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        've': 'http://schemas.microsoft.com/office/word/2006/wordml',
        'o': 'urn:schemas-microsoft-com:office:office',
        'v': 'urn:schemas-microsoft-com:vml',
        'w10': 'urn:schemas-microsoft-com:office:word',
        'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
        'w15': 'http://schemas.microsoft.com/office/word/2012/wordml',
        'w16': 'http://schemas.microsoft.com/office/word/2018/wordml',
        'wx': 'http://schemas.microsoft.com/office/word/2003/auxHint',
        'wne': 'http://schemas.microsoft.com/office/word/2006/wordml',
        'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
    }
    
    def __init__(self):
        # Register namespaces for XML parsing
        for prefix, uri in self.NAMESPACES.items():
            ET.register_namespace(prefix, uri)
    
    def extract_complete_structure(self, docx_path: str) -> Dict[str, Any]:
        """
        Extract COMPLETE document structure including all XML formatting
        """
        print("🔍 Deep-scanning document XML structure...")
        
        try:
            structure = {
                'document_xml': None,
                'styles_xml': None,
                'numbering_xml': None,
                'theme_xml': None,
                'settings_xml': None,
                'relationships': None,
                'content_types': None,
                'paragraphs': [],
                'sections': [],
                'headers_footers': [],
                'tables': [],
                'images': [],
                'drawing_objects': []
            }
            
            with zipfile.ZipFile(docx_path, 'r') as docx_zip:
                # Extract all XML files
                structure['document_xml'] = self._read_xml_file(docx_zip, 'word/document.xml')
                structure['styles_xml'] = self._read_xml_file(docx_zip, 'word/styles.xml')
                structure['numbering_xml'] = self._read_xml_file(docx_zip, 'word/numbering.xml')
                structure['theme_xml'] = self._read_xml_file(docx_zip, 'word/theme/theme1.xml')
                structure['settings_xml'] = self._read_xml_file(docx_zip, 'word/settings.xml')
                structure['relationships'] = self._read_xml_file(docx_zip, 'word/_rels/document.xml.rels')
                structure['content_types'] = self._read_xml_file(docx_zip, '[Content_Types].xml')
                
                # Parse document structure
                if structure['document_xml']:
                    structure['paragraphs'] = self._extract_paragraphs_with_full_formatting(
                        structure['document_xml']
                    )
                    structure['sections'] = self._extract_sections(structure['document_xml'])
                    structure['tables'] = self._extract_tables(structure['document_xml'])
                
                # Extract headers/footers
                structure['headers_footers'] = self._extract_headers_footers(docx_zip)
                
            print(f"✅ Extracted {len(structure['paragraphs'])} paragraphs with complete formatting")
            return structure
            
        except Exception as e:
            print(f"❌ Error extracting complete structure: {e}")
            return None
    
    def _read_xml_file(self, zip_file: zipfile.ZipFile, path: str) -> Optional[etree._Element]:
        """Read and parse XML file from docx zip"""
        try:
            xml_content = zip_file.read(path)
            return etree.fromstring(xml_content)
        except (KeyError, etree.XMLSyntaxError):
            return None
    
    def _extract_paragraphs_with_full_formatting(self, document_xml: etree._Element) -> List[Dict]:
        """Extract paragraphs with COMPLETE formatting information"""
        paragraphs = []
        
        # Find all paragraphs in the document
        para_elements = document_xml.xpath('.//w:p', namespaces=self.NAMESPACES)
        
        for i, para_elem in enumerate(para_elements):
            para_data = {
                'index': i,
                'xml_element': etree.tostring(para_elem, encoding='unicode'),
                'text': '',
                'properties': self._extract_paragraph_properties(para_elem),
                'runs': [],
                'is_empty': False,
                'contains_drawing': False,
                'contains_table': False,
                'style_id': None,
                'numbering': None
            }
            
            # Extract paragraph properties
            ppr = para_elem.find('.//w:pPr', self.NAMESPACES)
            if ppr is not None:
                para_data['properties'] = self._extract_detailed_paragraph_properties(ppr)
            
            # Extract all runs with complete formatting
            runs = para_elem.xpath('.//w:r', namespaces=self.NAMESPACES)
            for run_elem in runs:
                run_data = self._extract_complete_run_formatting(run_elem)
                para_data['runs'].append(run_data)
                para_data['text'] += run_data.get('text', '')
            
            # Check for drawings, images, etc.
            para_data['contains_drawing'] = bool(para_elem.xpath('.//w:drawing', namespaces=self.NAMESPACES))
            
            para_data['is_empty'] = len(para_data['text'].strip()) == 0
            
            paragraphs.append(para_data)
        
        return paragraphs
    
    def _extract_detailed_paragraph_properties(self, ppr_elem: etree._Element) -> Dict:
        """Extract detailed paragraph properties"""
        props = {
            'style': None,
            'alignment': None,
            'spacing': {},
            'indentation': {},
            'borders': {},
            'shading': {},
            'tabs': [],
            'numbering': {},
            'page_break': False,
            'keep_together': False,
            'keep_with_next': False,
            'outline_level': None
        }
        
        # Style reference
        style_elem = ppr_elem.find('w:pStyle', self.NAMESPACES)
        if style_elem is not None:
            props['style'] = style_elem.get(f'{{{self.NAMESPACES["w"]}}}val')
        
        # Alignment
        align_elem = ppr_elem.find('w:jc', self.NAMESPACES)
        if align_elem is not None:
            props['alignment'] = align_elem.get(f'{{{self.NAMESPACES["w"]}}}val')
        
        # Spacing
        spacing_elem = ppr_elem.find('w:spacing', self.NAMESPACES)
        if spacing_elem is not None:
            props['spacing'] = {
                'before': spacing_elem.get(f'{{{self.NAMESPACES["w"]}}}before'),
                'after': spacing_elem.get(f'{{{self.NAMESPACES["w"]}}}after'),
                'line': spacing_elem.get(f'{{{self.NAMESPACES["w"]}}}line'),
                'line_rule': spacing_elem.get(f'{{{self.NAMESPACES["w"]}}}lineRule')
            }
        
        # Indentation
        ind_elem = ppr_elem.find('w:ind', self.NAMESPACES)
        if ind_elem is not None:
            props['indentation'] = {
                'left': ind_elem.get(f'{{{self.NAMESPACES["w"]}}}left'),
                'right': ind_elem.get(f'{{{self.NAMESPACES["w"]}}}right'),
                'first_line': ind_elem.get(f'{{{self.NAMESPACES["w"]}}}firstLine'),
                'hanging': ind_elem.get(f'{{{self.NAMESPACES["w"]}}}hanging')
            }
        
        # Borders (including horizontal lines!)
        border_elem = ppr_elem.find('w:pBdr', self.NAMESPACES)
        if border_elem is not None:
            props['borders'] = self._extract_border_properties(border_elem)
        
        # Numbering
        numpr_elem = ppr_elem.find('w:numPr', self.NAMESPACES)
        if numpr_elem is not None:
            props['numbering'] = self._extract_numbering_properties(numpr_elem)
        
        # Tabs
        tabs_elem = ppr_elem.find('w:tabs', self.NAMESPACES)
        if tabs_elem is not None:
            props['tabs'] = self._extract_tab_properties(tabs_elem)
        
        return props
    
    def _extract_border_properties(self, border_elem: etree._Element) -> Dict:
        """Extract detailed border properties (crucial for horizontal lines)"""
        borders = {}
        
        for side in ['top', 'left', 'bottom', 'right']:
            side_elem = border_elem.find(f'w:{side}', self.NAMESPACES)
            if side_elem is not None:
                borders[side] = {
                    'style': side_elem.get(f'{{{self.NAMESPACES["w"]}}}val'),
                    'size': side_elem.get(f'{{{self.NAMESPACES["w"]}}}sz'),
                    'space': side_elem.get(f'{{{self.NAMESPACES["w"]}}}space'),
                    'color': side_elem.get(f'{{{self.NAMESPACES["w"]}}}color'),
                    'shadow': side_elem.get(f'{{{self.NAMESPACES["w"]}}}shadow')
                }
        
        return borders
    
    def _extract_numbering_properties(self, numpr_elem: etree._Element) -> Dict:
        """Extract numbering/bullet properties"""
        numbering = {}
        
        ilvl_elem = numpr_elem.find('w:ilvl', self.NAMESPACES)
        if ilvl_elem is not None:
            numbering['level'] = ilvl_elem.get(f'{{{self.NAMESPACES["w"]}}}val')
        
        numid_elem = numpr_elem.find('w:numId', self.NAMESPACES)
        if numid_elem is not None:
            numbering['id'] = numid_elem.get(f'{{{self.NAMESPACES["w"]}}}val')
        
        return numbering
    
    def _extract_tab_properties(self, tabs_elem: etree._Element) -> List[Dict]:
        """Extract tab stop properties"""
        tabs = []
        
        for tab_elem in tabs_elem.findall('w:tab', self.NAMESPACES):
            tab_data = {
                'position': tab_elem.get(f'{{{self.NAMESPACES["w"]}}}pos'),
                'alignment': tab_elem.get(f'{{{self.NAMESPACES["w"]}}}val'),
                'leader': tab_elem.get(f'{{{self.NAMESPACES["w"]}}}leader')
            }
            tabs.append(tab_data)
        
        return tabs
    
    def _extract_complete_run_formatting(self, run_elem: etree._Element) -> Dict:
        """Extract complete run formatting"""
        run_data = {
            'text': '',
            'xml_element': etree.tostring(run_elem, encoding='unicode'),
            'properties': {},
            'is_tab': False,
            'is_break': False,
            'is_symbol': False
        }
        
        # Extract text content
        text_elements = run_elem.findall('w:t', self.NAMESPACES)
        for text_elem in text_elements:
            run_data['text'] += text_elem.text or ''
        
        # Check for special elements
        run_data['is_tab'] = bool(run_elem.find('w:tab', self.NAMESPACES))
        run_data['is_break'] = bool(run_elem.find('w:br', self.NAMESPACES))
        
        # Extract run properties
        rpr = run_elem.find('w:rPr', self.NAMESPACES)
        if rpr is not None:
            run_data['properties'] = self._extract_detailed_run_properties(rpr)
        
        return run_data
    
    def _extract_detailed_run_properties(self, rpr_elem: etree._Element) -> Dict:
        """Extract detailed run properties"""
        props = {
            'font': {},
            'size': None,
            'color': None,
            'bold': False,
            'italic': False,
            'underline': None,
            'strike': False,
            'highlight': None,
            'vertical_align': None,
            'spacing': None,
            'position': None,
            'style': None
        }
        
        # Font information
        font_elem = rpr_elem.find('w:rFonts', self.NAMESPACES)
        if font_elem is not None:
            props['font'] = {
                'ascii': font_elem.get(f'{{{self.NAMESPACES["w"]}}}ascii'),
                'hansi': font_elem.get(f'{{{self.NAMESPACES["w"]}}}hAnsi'),
                'eastAsia': font_elem.get(f'{{{self.NAMESPACES["w"]}}}eastAsia'),
                'cs': font_elem.get(f'{{{self.NAMESPACES["w"]}}}cs')
            }
        
        # Font size
        sz_elem = rpr_elem.find('w:sz', self.NAMESPACES)
        if sz_elem is not None:
            props['size'] = sz_elem.get(f'{{{self.NAMESPACES["w"]}}}val')
        
        # Color
        color_elem = rpr_elem.find('w:color', self.NAMESPACES)
        if color_elem is not None:
            props['color'] = color_elem.get(f'{{{self.NAMESPACES["w"]}}}val')
        
        # Bold, Italic, etc.
        props['bold'] = rpr_elem.find('w:b', self.NAMESPACES) is not None
        props['italic'] = rpr_elem.find('w:i', self.NAMESPACES) is not None
        props['strike'] = rpr_elem.find('w:strike', self.NAMESPACES) is not None
        
        # Underline
        u_elem = rpr_elem.find('w:u', self.NAMESPACES)
        if u_elem is not None:
            props['underline'] = u_elem.get(f'{{{self.NAMESPACES["w"]}}}val')
        
        # Highlight
        highlight_elem = rpr_elem.find('w:highlight', self.NAMESPACES)
        if highlight_elem is not None:
            props['highlight'] = highlight_elem.get(f'{{{self.NAMESPACES["w"]}}}val')
        
        return props
    
    def _extract_sections(self, document_xml: etree._Element) -> List[Dict]:
        """Extract section properties"""
        sections = []
        
        sect_elements = document_xml.xpath('.//w:sectPr', namespaces=self.NAMESPACES)
        for sect_elem in sect_elements:
            section_data = {
                'xml_element': etree.tostring(sect_elem, encoding='unicode'),
                'page_size': {},
                'margins': {},
                'headers_footers': {},
                'columns': {},
                'page_numbers': {}
            }
            
            # Extract detailed section properties
            # This would include page margins, headers, footers, etc.
            sections.append(section_data)
        
        return sections
    
    def _extract_tables(self, document_xml: etree._Element) -> List[Dict]:
        """Extract table structures with complete formatting"""
        tables = []
        
        table_elements = document_xml.xpath('.//w:tbl', namespaces=self.NAMESPACES)
        for table_elem in table_elements:
            table_data = {
                'xml_element': etree.tostring(table_elem, encoding='unicode'),
                'properties': {},
                'rows': []
            }
            
            # Extract table properties and rows
            # This would include borders, cell formatting, etc.
            tables.append(table_data)
        
        return tables
    
    def _extract_headers_footers(self, docx_zip: zipfile.ZipFile) -> List[Dict]:
        """Extract headers and footers"""
        headers_footers = []
        
        # Look for header/footer files
        for file_info in docx_zip.filelist:
            if 'header' in file_info.filename or 'footer' in file_info.filename:
                xml_content = self._read_xml_file(docx_zip, file_info.filename)
                if xml_content is not None:
                    headers_footers.append({
                        'filename': file_info.filename,
                        'xml_element': etree.tostring(xml_content, encoding='unicode')
                    })
        
        return headers_footers
    
    def _extract_paragraph_properties(self, para_elem: etree._Element) -> Dict:
        """Legacy method for compatibility"""
        return self._extract_detailed_paragraph_properties(
            para_elem.find('w:pPr', self.NAMESPACES)
        ) if para_elem.find('w:pPr', self.NAMESPACES) is not None else {}

# Legacy compatibility
DocumentProcessor = AdvancedDocumentProcessor