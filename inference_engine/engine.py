# ============================================
# Custom Rule Engine
# Student Performance Prediction Advisor
# Built in Pure Python - No external libraries
# ============================================


# ============================================
# PART 1: FACT CLASS
# A Fact stores one piece of student data
# ============================================

class Fact:
    """
    Represents a single fact in the working memory.
    Example: Fact(attendance=68, midterm_score=55)
    """
    def __init__(self, **kwargs):
        self.data = kwargs

    def get(self, key, default=None):
        return self.data.get(key, default)

    def __repr__(self):
        return f"Fact({self.data})"


# ============================================
# PART 2: RULE CLASS
# A Rule has conditions (IF) and actions (THEN)
# ============================================

class Rule:
    """
    Represents a single rule in the knowledge base.

    Each rule has:
    - name        : unique rule identifier
    - conditions  : a function that checks IF part
    - actions     : a function that executes THEN part
    - cf          : certainty factor (0.0 to 1.0)
    - priority    : higher number = fires first
    - description : human readable explanation
    """
    def __init__(self, name, conditions, actions, cf=0.8,
                 priority=0, description=""):
        self.name        = name
        self.conditions  = conditions
        self.actions     = actions
        self.cf          = cf
        self.priority    = priority
        self.description = description
        self.fired       = False

    def __repr__(self):
        return f"Rule(name={self.name}, cf={self.cf})"


# ============================================
# PART 3: WORKING MEMORY
# Stores all current facts during reasoning
# ============================================

class WorkingMemory:
    """
    Working Memory holds all facts known so far.
    It grows as the inference engine fires rules
    and adds new conclusions.
    """
    def __init__(self):
        self.facts = {}

    def add(self, key, value):
        """Add a new fact to working memory"""
        self.facts[key] = value

    def get(self, key, default=None):
        """Get a fact value by key"""
        return self.facts.get(key, default)

    def has(self, key):
        """Check if a fact exists"""
        return key in self.facts

    def update(self, data: dict):
        """Add multiple facts at once"""
        self.facts.update(data)

    def get_all(self):
        """Return all facts"""
        return self.facts

    def __repr__(self):
        return f"WorkingMemory({self.facts})"


# ============================================
# PART 4: CERTAINTY FACTOR CALCULATOR
# Combines confidence scores mathematically
# ============================================

class CertaintyFactor:
    """
    Handles Certainty Factor arithmetic.

    CF Rules:
    - Both support same conclusion:
      CF_combined = CF1 + CF2 * (1 - CF1)

    - One supports, one opposes:
      CF_combined = CF1 + CF2 * (1 + CF1)

    - CF range: -1.0 (definitely false) to 1.0 (definitely true)
    """

    @staticmethod
    def combine_supporting(cf1, cf2):
        """
        Combine two CFs that BOTH support same conclusion.
        Example: attendance low (CF=0.8) AND grades low (CF=0.7)
                 both support HIGH RISK conclusion
        """
        return cf1 + cf2 * (1 - cf1)

    @staticmethod
    def combine_conflicting(cf1, cf2):
        """
        Combine two CFs where one supports and one opposes.
        Example: grades good (positive) BUT attendance bad (negative)
        """
        return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))

    @staticmethod
    def interpret(cf):
        """
        Convert CF number to human readable confidence level
        """
        if cf >= 0.9:
            return "Definite (90-100%)"
        elif cf >= 0.7:
            return "Very Likely (70-90%)"
        elif cf >= 0.5:
            return "Probable (50-70%)"
        elif cf >= 0.3:
            return "Possible (30-50%)"
        else:
            return "Uncertain (below 30%)"

    @staticmethod
    def to_percentage(cf):
        """Convert CF to percentage string"""
        return f"{int(cf * 100)}%"


# ============================================
# PART 5: CONFLICT RESOLVER
# Decides which rule fires when multiple rules
# can fire at the same time
# ============================================

class ConflictResolver:
    """
    Conflict Resolution Strategy:

    Priority Order:
    1. Rule priority number (higher = fires first)
    2. Certainty Factor (higher CF = fires first)
    3. Rule specificity (more conditions = fires first)
    4. Rule order in knowledge base (earlier = fires first)
    """

    @staticmethod
    def resolve(conflict_set):
        """
        Given a list of rules that can all fire,
        return them in the order they should fire.
        """
        if not conflict_set:
            return []

        # Sort by: priority DESC, then CF DESC
        sorted_rules = sorted(
            conflict_set,
            key=lambda rule: (rule.priority, rule.cf),
            reverse=True
        )

        return sorted_rules


# ============================================
# PART 6: EXPLANATION MODULE
# Records every step of reasoning
# ============================================

class ExplanationModule:
    """
    Records the complete reasoning chain.
    Every time a rule fires, we log:
    - Which rule fired
    - What conditions were true
    - What conclusion was reached
    - What CF value was assigned
    """

    def __init__(self):
        self.trace = []
        self.step  = 0

    def log(self, rule_name, description, conclusion, cf):
        """Log a single reasoning step"""
        self.step += 1
        entry = {
            "step"       : self.step,
            "rule"       : rule_name,
            "description": description,
            "conclusion" : conclusion,
            "cf"         : cf,
            "cf_label"   : CertaintyFactor.interpret(cf),
            "cf_percent" : CertaintyFactor.to_percentage(cf)
        }
        self.trace.append(entry)

    def get_trace(self):
        """Return complete reasoning trace"""
        return self.trace

    def print_trace(self):
        """Print reasoning chain in readable format"""
        print("\n" + "="*60)
        print("REASONING CHAIN / EXPLANATION")
        print("="*60)
        for entry in self.trace:
            print(f"\nStep {entry['step']}: {entry['rule']}")
            print(f"  Condition : {entry['description']}")
            print(f"  Conclusion: {entry['conclusion']}")
            print(f"  Confidence: {entry['cf_percent']} ({entry['cf_label']})")
        print("="*60)

    def clear(self):
        """Reset explanation for new student"""
        self.trace = []
        self.step  = 0


# ============================================
# PART 7: INFERENCE ENGINE
# The brain — runs forward chaining
# ============================================

class InferenceEngine:
    """
    Forward Chaining Inference Engine.

    Algorithm:
    1. Load student facts into Working Memory
    2. Find all rules whose conditions are satisfied
    3. Apply conflict resolution to order them
    4. Fire the highest priority rule
    5. Add new conclusions to Working Memory
    6. Repeat until no more rules can fire
    7. Return final conclusions + explanation
    """

    def __init__(self, knowledge_base):
        self.knowledge_base  = knowledge_base
        self.working_memory  = WorkingMemory()
        self.explanation     = ExplanationModule()
        self.conflict_resolver = ConflictResolver()
        self.fired_rules     = []

    def load_facts(self, student_data: dict):
        """Load initial student facts into working memory"""
        self.working_memory.update(student_data)

    def get_conflict_set(self):
        """
        Find all rules that:
        1. Have NOT been fired yet
        2. Have their conditions satisfied by current facts
        """
        conflict_set = []

        for rule in self.knowledge_base.get_rules():
            if not rule.fired:
                try:
                    if rule.conditions(self.working_memory):
                        conflict_set.append(rule)
                except Exception:
                    pass

        return conflict_set

    def run(self, student_data: dict):
        """
        Main forward chaining loop.
        Run until no more rules can fire.
        """
        # Reset everything for new student
        self.working_memory  = WorkingMemory()
        self.explanation     = ExplanationModule()
        self.fired_rules     = []

        # Reset all rules
        for rule in self.knowledge_base.get_rules():
            rule.fired = False

        # Load student data as initial facts
        self.load_facts(student_data)

        # Forward chaining loop
        iteration = 0
        max_iterations = 100  # Safety limit

        while iteration < max_iterations:
            iteration += 1

            # Step 1: Find all rules that can fire
            conflict_set = self.get_conflict_set()

            # Step 2: If no rules can fire, we are done
            if not conflict_set:
                break

            # Step 3: Apply conflict resolution
            ordered_rules = self.conflict_resolver.resolve(conflict_set)

            # Step 4: Fire the top priority rule
            rule_to_fire = ordered_rules[0]
            rule_to_fire.fired = True
            self.fired_rules.append(rule_to_fire)

            # Step 5: Execute rule actions
            # Actions add new facts to working memory
            rule_to_fire.actions(self.working_memory, self.explanation)

        # Return final results
        return self.get_results()

    def get_results(self):
        """
        Compile final results from working memory
        """
        wm = self.working_memory

        results = {
            "performance_level" : wm.get("performance_level", "Unknown"),
            "risk_level"        : wm.get("risk_level", "Unknown"),
            "risk_score"        : wm.get("risk_score", 0),
            "confidence"        : wm.get("confidence", 0.0),
            "primary_factors"   : wm.get("primary_factors", []),
            "recommendations"   : wm.get("recommendations", []),
            "reasoning_trace"   : self.explanation.get_trace(),
            "fired_rules_count" : len(self.fired_rules),
            "fired_rules"       : [r.name for r in self.fired_rules]
        }

        return results


# ============================================
# PART 8: KNOWLEDGE BASE
# Holds all rules — will be filled with
# 60+ rules in the next file
# ============================================

class KnowledgeBase:
    """
    Stores all rules for the expert system.
    Rules are loaded from rules.py
    """

    def __init__(self):
        self.rules = []

    def add_rule(self, rule: Rule):
        """Add a single rule to the knowledge base"""
        self.rules.append(rule)

    def add_rules(self, rules: list):
        """Add multiple rules at once"""
        self.rules.extend(rules)

    def get_rules(self):
        """Return all rules"""
        return self.rules

    def get_rule_count(self):
        """Return total number of rules"""
        return len(self.rules)

    def find_rule(self, name):
        """Find a specific rule by name"""
        for rule in self.rules:
            if rule.name == name:
                return rule
        return None

    def __repr__(self):
        return f"KnowledgeBase({len(self.rules)} rules)"