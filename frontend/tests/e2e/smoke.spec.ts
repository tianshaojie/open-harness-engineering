import { expect, test } from "@playwright/test"

test("playground route is reachable and interactive", async ({ page }) => {
  await page.goto("/playground")

  await expect(page.getByRole("heading", { name: "Playground", exact: true })).toBeVisible()
  await expect(page.getByTestId("playground-counter")).toContainText("Counter: 0")

  await page.getByRole("button", { name: "Increment" }).click()
  await expect(page.getByTestId("playground-counter")).toContainText("Counter: 1")
})
