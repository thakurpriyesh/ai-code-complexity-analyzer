import re

try:
    from radon.complexity import cc_visit
    RADON_AVAILABLE = True
except ImportError:
    RADON_AVAILABLE = False

def extract_features_heuristics(code_str, language):
    """Extracts structural features, variables, and code composition."""
    code_str_lower = code_str.lower()
    raw_lines = code_str.split('\n')
    total_lines = len(raw_lines)
    
    blank_lines = len([line for line in raw_lines if line.strip() == ''])
    comments = len(re.findall(r'(#|//|/\*|\*/)', code_str))
    actual_code_lines = max(0, total_lines - blank_lines - comments)
    
    loops = len(re.findall(r'\b(for|while|do)\b', code_str_lower))
    conditionals = len(re.findall(r'\b(if|else|elif|switch|case)\b', code_str_lower))
    variables = len(re.findall(r'\b[a-zA-Z_]\w*\s*=\s*[^=]', code_str))
    classes = len(re.findall(r'\bclass\b', code_str_lower))
    
    if language == "Python":
        functions = len(re.findall(r'\bdef\b', code_str_lower))
    elif language == "JavaScript":
        functions = len(re.findall(r'\b(function|=>)\b', code_str_lower))
    else: 
        functions = len(re.findall(r'\b(void|int|public|private|String)\s+\w+\s*\(', code_str))
        
    max_depth = 0
    current_depth = 0
    for char in code_str:
        if char == '{': current_depth += 1
        elif char == '}': current_depth = max(0, current_depth - 1)
        max_depth = max(max_depth, current_depth)
        
    if language == "Python":
        max_depth = max([len(line) - len(line.lstrip()) for line in raw_lines if line.strip()] + [0]) // 4
        
    if loops == 0: time_complexity = "O(1) or O(log n)"
    elif max_depth <= 1: time_complexity = "O(n)"
    elif max_depth == 2: time_complexity = "O(n^2)"
    else: time_complexity = "O(n^3) or higher"
        
    return {
        'loops': loops, 'conditionals': conditionals, 'functions': functions,
        'variables': variables, 'classes': classes, 'total_lines': total_lines, 
        'actual_code_lines': actual_code_lines, 'comments': comments, 
        'blank_lines': blank_lines, 'max_depth': max_depth, 'time_complexity': time_complexity
    }

def get_actual_complexity(code_str, language):
    """Uses radon to calculate actual cyclomatic complexity (Python only)."""
    if language != "Python" or not RADON_AVAILABLE: return "N/A (Python Only)"
    try:
        blocks = cc_visit(code_str)
        complexity = sum([block.complexity for block in blocks])
        return complexity if complexity > 0 else 1
    except Exception: return 1