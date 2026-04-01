export interface ShellNavItem {
  label: string
  to: string
  badge?: string
  disabled?: boolean
}

export interface ShellNavGroup {
  title: string
  items: ShellNavItem[]
}

export const sidebarNavGroups: ShellNavGroup[] = [
  {
    title: "Foundation",
    items: [
      { label: "Overview", to: "/" },
      { label: "Playground", to: "/playground" }
    ]
  },
  {
    title: "AI Workspace",
    items: [
      { label: "Design Sandbox", to: "/", badge: "Soon", disabled: true },
      { label: "QA Desk", to: "/", badge: "Soon", disabled: true }
    ]
  },
  {
    title: "Operations",
    items: [
      { label: "Runbook Console", to: "/", badge: "Soon", disabled: true }
    ]
  }
]

export const topNavItems: ShellNavItem[] = [
  { label: "Overview", to: "/" },
  { label: "Playground", to: "/playground" }
]
