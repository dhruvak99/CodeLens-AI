import {
  Bot,
  BrainCircuit,
  Braces,
  Code2,
  Database,
  GitBranch,
  Gauge,
  GraduationCap,
  Route,
  Rows3,
  SearchCheck,
  Sparkles,
  Wrench
} from "lucide-react";

export const navItems = [
  { label: "Features", href: "#features" },
  { label: "Workspaces", href: "#workspaces" },
  { label: "Architecture", href: "#architecture" },
  { label: "GitHub", href: "https://github.com/dhruvak99/CodeLens-AI" }
];

export const features = [
  {
    title: "Semantic Analysis",
    description:
      "Understand Python intent, data flow, and logic issues beyond syntax.",
    icon: BrainCircuit
  },
  {
    title: "Runtime Execution",
    description:
      "Step through Python execution with variable state and line-level context.",
    icon: Route
  },
  {
    title: "AI Explain",
    description:
      "Turn analyzer findings into clear Python learning guidance.",
    icon: Sparkles
  },
  {
    title: "Suggested Fixes",
    description:
      "Review focused corrections for logic, maintainability, and code quality.",
    icon: Wrench
  },
  {
    title: "Complexity Metrics",
    description:
      "Surface time, space, and cyclomatic complexity as you code.",
    icon: Gauge
  },
  {
    title: "Semantic Graph",
    description:
      "Map control flow, semantic relationships, and execution dependencies.",
    icon: GitBranch
  },
  {
    title: "Natural Language SQL",
    description:
      "Convert learning prompts into validated SQL with schema-aware generation.",
    icon: Code2
  },
  {
    title: "Dataset Explorer",
    description:
      "Browse live tables, rows, and dataset previews before writing queries.",
    icon: Database
  },
  {
    title: "Schema Browser",
    description:
      "Inspect table columns, types, and keys while learning SQL concepts.",
    icon: Braces
  },
  {
    title: "SQL Validation",
    description:
      "Check generated SQL against real tables and columns before execution.",
    icon: SearchCheck
  },
  {
    title: "Live Query Results",
    description:
      "Execute SQL safely and inspect dynamic result tables in the lab.",
    icon: Rows3
  },
  {
    title: "AI SQL Tutor",
    description:
      "Learn each generated query through beginner-friendly Qwen2.5 tutoring.",
    icon: GraduationCap
  }
];

export const workspaceCards = [
  {
    title: "Python Lab",
    description:
      "Learn Python through semantic analysis, runtime visualization, AI explanations, and interactive debugging.",
    features: [
      "Semantic Analysis",
      "Runtime Trace",
      "AI Explanations",
      "Suggested Fixes",
      "Complexity Metrics",
      "Interactive Semantic Graph"
    ],
    button: "Explore Python Lab"
  },
  {
    title: "SQL Lab",
    description:
      "Learn SQL by converting natural language into SQL, exploring datasets, validating queries, and understanding every statement with an AI tutor.",
    features: [
      "Natural Language -> SQL",
      "Live Dataset Explorer",
      "Schema Visualization",
      "SQL Validation",
      "Live Query Execution",
      "AI SQL Tutor (powered by Qwen2.5)"
    ],
    button: "Explore SQL Lab"
  }
];

export const architectureBranches = [
  {
    workspace: "Python Lab",
    steps: ["Semantic Engine", "Runtime Engine", "Complexity Metrics", "AI Explain"]
  },
  {
    workspace: "SQL Lab",
    steps: ["SemanticSQL", "SQL Validator", "SQL Execution", "AI SQL Tutor"]
  }
];

export const findings = [
  {
    title: "Potential Index Error",
    severity: "High",
    detail: "Accessing arr[mid] can fail when the input array is empty.",
    tone: "red"
  },
  {
    title: "Missing Type Hints",
    severity: "Medium",
    detail: "Function parameters are untyped, reducing semantic confidence.",
    tone: "amber"
  },
  {
    title: "Unnecessary Else",
    severity: "Low",
    detail: "The else block after return can be flattened for readability.",
    tone: "blue"
  }
];

export const demoFindings = [
  "Semantic Analysis",
  "Runtime Trace",
  "AI Explanation"
];

export const sqlDemoSteps = [
  "Question: \"Show students with CGPA above 8\"",
  "Generated SQL",
  "Execution Result",
  "AI SQL Tutor Explanation"
];

export const codeLines = [
  "def binary_search(arr, target):",
  "    low, high = 0, len(arr) - 1",
  "",
  "    while low <= high:",
  "        mid = (low + high) // 2",
  "        if arr[mid] == target:",
  "            return mid",
  "        elif arr[mid] < target:",
  "            low = mid + 1",
  "        else:",
  "            high = mid - 1",
  "    return -1"
];

export const demoCode = `def score_window(values):
    total = 0
    for value in values:
        total += value

    average = total / len(values)
    if average > 75:
        return "strong"
    else:
        return "review"`;

export const footerLinks = [
  { label: "GitHub", href: "https://github.com/dhruvak99/CodeLens-AI" },
  { label: "Documentation", href: "#docs" },
  { label: "Version", href: "#version" }
];

export const logoIcon = Bot;
