import ast
import re

def analyze_code(code):
    suggestions = []
    
    # Try to parse the code
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"Syntax error at line {e.lineno}: {e.msg}"]
    
    # Analyze using AST
    suggestions.extend(check_unused_variables(tree, code))
    suggestions.extend(check_bad_practices(tree))
    suggestions.extend(check_possible_bugs(tree))
    suggestions.extend(check_code_smells(code))
    
    if not suggestions:
        suggestions.append("Code looks good. No major issues detected.")
    
    return suggestions


def check_unused_variables(tree, code):
    suggestions = []
    assigned = set()
    used = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned.add(target.id)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)
    
    unused = assigned - used
    if unused:
        suggestions.append(f"Unused variables detected: {', '.join(sorted(unused))}")
    
    return suggestions


def check_bad_practices(tree):
    suggestions = []
    
    for node in ast.walk(tree):
        # Bare except
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            suggestions.append("Avoid bare 'except:' clauses. Catch specific exceptions instead.")
        
        # Using 'eval' or 'exec'
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ('eval', 'exec'):
                suggestions.append(f"Avoid using '{node.func.id}()'. It can be a security risk.")
        
        # Mutable default arguments
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    suggestions.append(f"Function '{node.name}' has mutable default argument. Use None instead.")
        
        # Global statement usage
        if isinstance(node, ast.Global):
            suggestions.append("Avoid using 'global' keyword. Consider refactoring to use function parameters.")
    
    return suggestions


def check_possible_bugs(tree):
    suggestions = []
    
    for node in ast.walk(tree):
        # Comparison with True/False
        if isinstance(node, ast.Compare):
            for comparator in node.comparators:
                if isinstance(comparator, ast.Constant) and comparator.value in (True, False):
                    suggestions.append("Avoid comparing with True/False. Use 'if variable:' instead.")
        
        # Assignment in condition (common typo)
        if isinstance(node, ast.If):
            if isinstance(node.test, ast.NamedExpr):
                suggestions.append("Assignment in condition detected. Make sure this is intentional.")
        
        # Empty except block
        if isinstance(node, ast.ExceptHandler):
            if not node.body or (len(node.body) == 1 and isinstance(node.body[0], ast.Pass)):
                suggestions.append("Empty except block detected. Handle exceptions properly.")
    
    return suggestions


def check_code_smells(code):
    suggestions = []
    
    # Too many print statements
    print_count = code.count('print(')
    if print_count > 5:
        suggestions.append(f"Found {print_count} print statements. Consider using logging module.")
    
    # Long lines
    lines = code.split('\n')
    long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 100]
    if long_lines:
        suggestions.append(f"Lines too long (>100 chars): {', '.join(map(str, long_lines[:3]))}")
    
    # TODO/FIXME comments
    if re.search(r'#.*\b(TODO|FIXME)\b', code, re.IGNORECASE):
        suggestions.append("Found TODO/FIXME comments. Consider addressing them.")
    
    return suggestions
