"""
Custom Rules System - Core implementation
"""

import re
from typing import Dict, Any, List, Callable
from bs4 import BeautifulSoup


class ExtractionRule:
    def __init__(self, 
                 name: str,
                 field: str,
                 condition: Callable[[str, Dict[str, Any]], bool],
                 action: Callable[[str, Dict[str, Any]], Any],
                 priority: int = 0):
        self.name = name
        self.field = field
        self.condition = condition
        self.action = action
        self.priority = priority
    
    def can_apply(self, html: str, data: Dict[str, Any]) -> bool:
        try:
            return self.condition(html, data)
        except Exception:
            return False
    
    def apply(self, html: str, data: Dict[str, Any]) -> Any:
        try:
            return self.action(html, data)
        except Exception as e:
            print(f"❌ Error applying rule {self.name}: {e}")
            return None


class CustomExtractor:
    def __init__(self):
        self.pre_hooks: List[Callable] = []
        self.post_hooks: List[Callable] = []
        self.rules: Dict[str, List[ExtractionRule]] = {}
    
    def add_pre_hook(self, hook: Callable[[str, Dict[str, Any]], tuple]):
        self.pre_hooks.append(hook)
    
    def add_post_hook(self, hook: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.post_hooks.append(hook)
    
    def add_rule(self, rule: ExtractionRule):
        if rule.field not in self.rules:
            self.rules[rule.field] = []
        self.rules[rule.field].append(rule)
        self.rules[rule.field].sort(key=lambda r: r.priority, reverse=True)
    
    def extract_with_rules(self, html: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Run pre-hooks
        for hook in self.pre_hooks:
            try:
                html, data = hook(html, data)
            except Exception as e:
                print(f"❌ Error in pre-hook: {e}")
        
        # Apply extraction rules
        for field, rules in self.rules.items():
            for rule in rules:
                if rule.can_apply(html, data):
                    value = rule.apply(html, data)
                    if value is not None:
                        data[field] = value
                        print(f"✅ Applied rule '{rule.name}' for field '{field}': {value}")
                        break
        
        # Run post-hooks
        for hook in self.post_hooks:
            try:
                data = hook(data)
            except Exception as e:
                print(f"❌ Error in post-hook: {e}")
        
        return data


class RuleBuilder:
    @staticmethod
    def css_selector_rule(name: str, field: str, selector: str, 
                         attribute: str = 'text', priority: int = 0) -> ExtractionRule:
        def condition(html: str, data: Dict[str, Any]) -> bool:
            soup = BeautifulSoup(html, 'html.parser')
            return soup.select_one(selector) is not None
        
        def action(html: str, data: Dict[str, Any]) -> str:
            soup = BeautifulSoup(html, 'html.parser')
            element = soup.select_one(selector)
            if element:
                if attribute == 'text':
                    return element.get_text(strip=True)
                else:
                    return element.get(attribute, '')
            return None
        
        return ExtractionRule(name, field, condition, action, priority)
    
    @staticmethod
    def regex_rule(name: str, field: str, pattern: str, 
                   group: int = 1, priority: int = 0) -> ExtractionRule:
        def condition(html: str, data: Dict[str, Any]) -> bool:
            return bool(re.search(pattern, html, re.IGNORECASE))
        
        def action(html: str, data: Dict[str, Any]) -> str:
            match = re.search(pattern, html, re.IGNORECASE)
            if match and len(match.groups()) >= group:
                return match.group(group)
            return None
        
        return ExtractionRule(name, field, condition, action, priority)
    
    @staticmethod
    def url_condition_rule(name: str, field: str, url_pattern: str,
                          extract_func: Callable[[str, Dict[str, Any]], Any],
                          priority: int = 0) -> ExtractionRule:
        def condition(html: str, data: Dict[str, Any]) -> bool:
            url = data.get('url', '')
            return bool(re.search(url_pattern, url))
        
        return ExtractionRule(name, field, condition, extract_func, priority)