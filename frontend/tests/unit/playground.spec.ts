import { mount } from "@vue/test-utils"
import { describe, expect, it } from "vitest"

import PlaygroundCard from "@/components/playground/PlaygroundCard.vue"

describe("PlaygroundCard", () => {
  it("increments counter when button is clicked", async () => {
    const wrapper = mount(PlaygroundCard)

    expect(wrapper.get('[data-testid="playground-counter"]').text()).toContain("Counter: 0")

    await wrapper.get("button").trigger("click")

    expect(wrapper.get('[data-testid="playground-counter"]').text()).toContain("Counter: 1")
  })
})
