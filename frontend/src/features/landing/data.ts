import {
  Bot,
  BrainCircuit,
  GitBranch,
  Gauge,
  Route,
  Sparkles,
  Wrench
} from "lucide-react";

export const navItems = [
  { label: "Features", href: "#features" },
  { label: "Architecture", href: "#architecture" },
  { label: "Docs", href: "#docs" },
  { label: "GitHub", href: "https://github.com" }
];

export const features = [
  {
    title: "Semantic Analysis",
    description:
      "Detect intent, data flow, and logic issues beyond surface-level syntax.",
    icon: BrainCircuit
  },
  {
    title: "Runtime Trace",
    description:
      "Step through execution paths with variable state and line-level context.",
    icon: Route
  },
  {
    title: "AI Explanations",
    description:
      "Turn findings into clear reasoning that helps developers learn faster.",
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
      "Surface time, space, and cyclomatic complexity where decisions happen.",
    icon: Gauge
  },
  {
    title: "Interactive Graphs",
    description:
      "Map control flow, semantic relationships, and execution dependencies.",
    icon: GitBranch
  }
];

export const architectureSteps = [
  "Editor",
  "Analysis Engine",
  "Semantic Graph",
  "Findings",
  "AI Explain"
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
  "Guard against empty arrays before entering the loop.",
  "Add explicit parameter and return annotations.",
  "Prefer a direct return path after the target match branch."
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
  { label: "GitHub", href: "https://github.com" },
  { label: "Documentation", href: "#docs" },
  { label: "Version", href: "#version" }
];

export const logoIcon = Bot;
