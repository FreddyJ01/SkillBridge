"""
Precision formatting validator to ensure perfect resume formatting
"""

from lxml import etree
from typing import Dict, List, Tuple
import re

class FormattingValidator:
    """
    Validates that formatting has been perfectly preserved
    """
    
    def __init__(self, namespaces: Dict[str, str]):
        self.namespaces = namespaces
    
    def validate_formatting_preservation(self, original_paragraphs: List[Dict], 
                                       modified_paragraphs: List[etree._Element]) -> Dict:
        """
        Comprehensive validation of formatting preservation
        """
        validation_results = {
            'overall_score': 0.0,
            'issues_found': [],
            'formatting_matches': [],
            'recommendations': []
        }
        
        try:
            print("🔍 Validating formatting preservation...")
            
            total_checks = 0
            passed_checks = 0
            
            # Compare each paragraph
            for i, (original, modified) in enumerate(zip(original_paragraphs, modified_paragraphs)):
                paragraph_score, issues = self._validate_paragraph_formatting(
                    original, modified, i
                )
                
                validation_results['formatting_matches'].append({
                    'paragraph_index': i,
                    'score': paragraph_score,
                    'issues': issues
                })
                
                total_checks += 1
                if paragraph_score >= 0.95:  # 95% threshold for "perfect"
                    passed_checks += 1
                else:
                    validation_results['issues_found'].extend(issues)
            
            # Calculate overall score
            validation_results['overall_score'] = (passed_checks / total_checks) if total_checks > 0 else 0.0
            
            # Generate recommendations
            validation_results['recommendations'] = self._generate_recommendations(
                validation_results['issues_found']
            )
            
            print(f"📊 Formatting validation score: {validation_results['overall_score']:.1%}")
            
            return validation_results
            
        except Exception as e:
            print(f"⚠️  Validation error: {e}")
            return validation_results
    
    def _validate_paragraph_formatting(self, original: Dict, 
                                     modified: etree._Element, index: int) -> Tuple[float, List[str]]:
        """
        Validate formatting for a single paragraph
        """
        issues = []
        checks_passed = 0
        total_checks = 0
        
        # Check paragraph properties
        para_score, para_issues = self._check_paragraph_properties(original, modified)
        issues.extend(para_issues)
        checks_passed += para_score
        total_checks += 1
        
        # Check run formatting
        run_score, run_issues = self._check_run_formatting(original, modified)
        issues.extend(run_issues)
        checks_passed += run_score
        total_checks += 1
        
        # Check indentation and spacing
        indent_score, indent_issues = self._check_indentation_spacing(original, modified)
        issues.extend(indent_issues)
        checks_passed += indent_score
        total_checks += 1
        
        # Check borders and shading
        border_score, border_issues = self._check_borders_shading(original, modified)
        issues.extend(border_issues)
        checks_passed += border_score
        total_checks += 1
        
        final_score = checks_passed / total_checks if total_checks > 0 else 0.0
        return final_score, issues
    
    def _check_paragraph_properties(self, original: Dict, 
                                  modified: etree._Element) -> Tuple[float, List[str]]:
        """Check paragraph-level properties"""
        issues = []
        score = 1.0
        
        try:
            original_props = original.get('properties', {})
            
            # Get modified paragraph properties
            ppr = modified.find('w:pPr', self.namespaces)
            
            # Check alignment
            original_alignment = original_props.get('alignment')
            if original_alignment and ppr is not None:
                jc_elem = ppr.find('w:jc', self.namespaces)
                if jc_elem is not None:
                    modified_alignment = jc_elem.get(f'{{{self.namespaces["w"]}}}val')
                    if original_alignment != modified_alignment:
                        issues.append(f"Alignment mismatch: {original_alignment} vs {modified_alignment}")
                        score -= 0.2
                elif original_alignment != 'left':  # Default is left
                    issues.append(f"Missing alignment: expected {original_alignment}")
                    score -= 0.2
            
            # Check numbering
            original_numbering = original_props.get('numbering')
            if original_numbering and ppr is not None:
                num_pr = ppr.find('w:numPr', self.namespaces)
                if num_pr is None:
                    issues.append("Missing numbering properties")
                    score -= 0.3
            
            return max(0.0, score), issues
            
        except Exception as e:
            return 0.5, [f"Error checking paragraph properties: {e}"]
    
    def _check_run_formatting(self, original: Dict, 
                            modified: etree._Element) -> Tuple[float, List[str]]:
        """Check run-level formatting"""
        issues = []
        score = 1.0
        
        try:
            original_runs = original.get('runs', [])
            modified_runs = modified.xpath('.//w:r', namespaces=self.namespaces)
            
            if len(original_runs) != len(modified_runs):
                # This might be OK if content changed but formatting is preserved
                # We'll check if formatting patterns are maintained
                pass
            
            # Check key formatting properties in the first few runs
            for i, original_run in enumerate(original_runs[:3]):  # Check first 3 runs
                if i < len(modified_runs):
                    run_score = self._compare_run_formatting(original_run, modified_runs[i])
                    score *= run_score
            
            return max(0.0, score), issues
            
        except Exception as e:
            return 0.5, [f"Error checking run formatting: {e}"]
    
    def _compare_run_formatting(self, original_run: Dict, 
                              modified_run: etree._Element) -> float:
        """Compare formatting between original and modified runs"""
        
        original_props = original_run.get('properties', {})
        
        # Get modified run properties
        rpr = modified_run.find('w:rPr', self.namespaces)
        
        score = 1.0
        
        # Check bold
        original_bold = original_props.get('bold', False)
        modified_bold = rpr is not None and rpr.find('w:b', self.namespaces) is not None
        
        if original_bold != modified_bold:
            score -= 0.3
        
        # Check italic
        original_italic = original_props.get('italic', False)
        modified_italic = rpr is not None and rpr.find('w:i', self.namespaces) is not None
        
        if original_italic != modified_italic:
            score -= 0.3
        
        # Check font size
        original_size = original_props.get('size')
        if original_size and rpr is not None:
            sz_elem = rpr.find('w:sz', self.namespaces)
            if sz_elem is not None:
                modified_size = sz_elem.get(f'{{{self.namespaces["w"]}}}val')
                if original_size != modified_size:
                    score -= 0.2
        
        return max(0.0, score)
    
    def _check_indentation_spacing(self, original: Dict, 
                                 modified: etree._Element) -> Tuple[float, List[str]]:
        """Check indentation and spacing properties"""
        issues = []
        score = 1.0
        
        try:
            original_props = original.get('properties', {})
            
            # Get paragraph properties
            ppr = modified.find('w:pPr', self.namespaces)
            
            # Check indentation
            original_indent = original_props.get('indentation', {})
            if original_indent and ppr is not None:
                ind_elem = ppr.find('w:ind', self.namespaces)
                
                for indent_attr in ['left', 'right', 'firstLine', 'hanging']:
                    original_value = original_indent.get(indent_attr)
                    if original_value:
                        if ind_elem is not None:
                            modified_value = ind_elem.get(f'{{{self.namespaces["w"]}}}{indent_attr}')
                            if str(original_value) != str(modified_value):
                                issues.append(f"Indentation mismatch ({indent_attr}): {original_value} vs {modified_value}")
                                score -= 0.25
                        else:
                            issues.append(f"Missing indentation element for {indent_attr}")
                            score -= 0.25
            
            # Check spacing
            original_spacing = original_props.get('spacing', {})
            if original_spacing and ppr is not None:
                spacing_elem = ppr.find('w:spacing', self.namespaces)
                
                for spacing_attr in ['before', 'after', 'line']:
                    original_value = original_spacing.get(spacing_attr)
                    if original_value:
                        if spacing_elem is not None:
                            modified_value = spacing_elem.get(f'{{{self.namespaces["w"]}}}{spacing_attr}')
                            if str(original_value) != str(modified_value):
                                issues.append(f"Spacing mismatch ({spacing_attr}): {original_value} vs {modified_value}")
                                score -= 0.25
                        else:
                            issues.append(f"Missing spacing element for {spacing_attr}")
                            score -= 0.25
            
            return max(0.0, score), issues
            
        except Exception as e:
            return 0.5, [f"Error checking indentation/spacing: {e}"]
    
    def _check_borders_shading(self, original: Dict, 
                             modified: etree._Element) -> Tuple[float, List[str]]:
        """Check borders and shading"""
        issues = []
        score = 1.0
        
        try:
            original_props = original.get('properties', {})
            
            # Get paragraph properties
            ppr = modified.find('w:pPr', self.namespaces)
            
            # Check borders
            original_borders = original_props.get('borders')
            if original_borders and ppr is not None:
                pBdr = ppr.find('w:pBdr', self.namespaces)
                if pBdr is None:
                    issues.append("Missing paragraph borders")
                    score -= 0.5
                else:
                    # Check specific border properties
                    for border_side in ['top', 'bottom', 'left', 'right']:
                        if border_side in original_borders:
                            border_elem = pBdr.find(f'w:{border_side}', self.namespaces)
                            if border_elem is None:
                                issues.append(f"Missing {border_side} border")
                                score -= 0.25
            
            # Check shading
            original_shading = original_props.get('shading')
            if original_shading and ppr is not None:
                shd_elem = ppr.find('w:shd', self.namespaces)
                if shd_elem is None:
                    issues.append("Missing paragraph shading")
                    score -= 0.3
            
            return max(0.0, score), issues
            
        except Exception as e:
            return 0.5, [f"Error checking borders/shading: {e}"]
    
    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate recommendations based on found issues"""
        recommendations = []
        
        issue_patterns = {
            'alignment': 'Consider preserving original paragraph alignment settings',
            'indentation': 'Verify indentation values are copied exactly from original',
            'spacing': 'Check that line spacing and paragraph spacing match original',
            'borders': 'Ensure paragraph borders and horizontal lines are preserved',
            'bold': 'Verify bold formatting is applied consistently',
            'italic': 'Check italic formatting preservation',
            'numbering': 'Preserve original numbering and bullet point formatting'
        }
        
        for pattern, recommendation in issue_patterns.items():
            if any(pattern.lower() in issue.lower() for issue in issues):
                if recommendation not in recommendations:
                    recommendations.append(recommendation)
        
        if not recommendations:
            recommendations.append("Formatting appears to be well preserved!")
        
        return recommendations