# Example rewrite output (synthetic test)

This file is a **sandbox demonstration** of what Cursor subagents should produce when rewriting ADAPTT-style prose **in place**. It is not a real ADAPTT page.

You get three views of the same transformation:

1. **Full before** and **full after** in normal paragraph layout (what a reader sees).
2. **Line changes** as a unified `diff -u` (what you track in git). The diff uses **one sentence per line** so each removal or addition stays easy to follow.

For copy-paste agent workflows, see [`SUBAGENT_PROMPTS.md`](SUBAGENT_PROMPTS.md).

---

## Full before (synthetic article)

### Why go vegan?

Compassionate people often adopt a vegan lifestyle because they want to reduce animal suffering. For many, it starts with learning about cruelty on factory farms.

Plant-based eating is a practical way to minimise harm while you learn. You can swap in vegan options at your own pace. Every step counts toward a kinder world.

Some consumers choose humane and free-range products to support better conditions. That can be a bridge while you transition. Reducing harm matters, even if you are not perfect yet.

Nobody should feel guilty for doing their best. Veganism is about progress, not purity. When you are ready, you can deepen your commitment.

If you want recipes and tips, start with small changes. Going vegan is a journey, and you can celebrate each win along the way.

---

## Full after (publish-ready replacement)

### Why act on the recognition?

Many people confront what we do to other animals through compassion first, especially after footage from farms and slaughter exposes routine separation, confinement, mutilation, and killing on schedules we impose. Outrage at suffering is a sane response, but it is not the whole claim. Veganism is the recognition that no human has the right to exploit other animals. That duty does not wait on your feelings.

Exploitation is not a mood problem. It is the relationship where we treat someone else’s life and body like inventory we may breed, rearrange, confine, take milk or eggs from, display, gamble on in labs, and kill when usefulness slips. Pain makes the injustice vivid, yet exploitation without theatrical suffering is still exploitation. A calm cow who is milked gently is still impregnated and milked without her agreement on a timetable we set because we assumed we owned her.

Labels such as humane, cage-free, or free-range negotiate the interior decoration of injustice. Even if marketing claims held completely, other animals remain owned and scheduled toward our profit cycles and death dates. Buying the kinder SKU does not answer the abolition challenge. Closing that exit means naming the structural wrong, not debating which cage is prettier.

Practice can shift unevenly in the real economy, and shame usually slows people down. Still, separate material difficulty from moral permission. The obligation is immediate and universal, and practical life becomes the work of closing the gap between that recognition and ordinary decisions about meals, textiles, cosmetics, travel, sport, media, and nightlife when those routes still treat other animals as resources.

Recipes, clothing swaps, and travel tips can be useful once the recognition leads. They describe how the principle shows up in life; they are not what the principle is. Keep the steps practical, keep the argument structural, and keep the demand universal.

---

## Line changes (unified diff)

Each line below is **one sentence**, matching how you might format prose for clearer `git diff` reviews. Paths are illustrative.

```diff
--- example-before.txt
+++ example-after.txt
@@ -1,19 +1,24 @@
-# Why go vegan?
+# Why act on the recognition?

 
-Compassionate people often adopt a vegan lifestyle because they want to reduce animal suffering.
-For many, it starts with learning about cruelty on factory farms.
+Many people confront what we do to other animals through compassion first, especially after footage from farms and slaughter exposes routine separation, confinement, mutilation, and killing on schedules we impose.
+Outrage at suffering is a sane response, but it is not the whole claim.
+Veganism is the recognition that no human has the right to exploit other animals.
+That duty does not wait on your feelings.
 
-Plant-based eating is a practical way to minimise harm while you learn.
-You can swap in vegan options at your own pace.
-Every step counts toward a kinder world.
+Exploitation is not a mood problem.
+It is the relationship where we treat someone else’s life and body like inventory we may breed, rearrange, confine, take milk or eggs from, display, gamble on in labs, and kill when usefulness slips.
+Pain makes the injustice vivid, yet exploitation without theatrical suffering is still exploitation.
+A calm cow who is milked gently is still impregnated and milked without her agreement on a timetable we set because we assumed we owned her.
 
-Some consumers choose humane and free-range products to support better conditions.
-That can be a bridge while you transition.
-Reducing harm matters, even if you are not perfect yet.
+Labels such as humane, cage-free, or free-range negotiate the interior decoration of injustice.
+Even if marketing claims held completely, other animals remain owned and scheduled toward our profit cycles and death dates.
+Buying the kinder SKU does not answer the abolition challenge.
+Closing that exit means naming the structural wrong, not debating which cage is prettier.
 
-Nobody should feel guilty for doing their best.
-Veganism is about progress, not purity.
-When you are ready, you can deepen your commitment.
+Practice can shift unevenly in the real economy, and shame usually slows people down.
+Still, separate material difficulty from moral permission.
+The obligation is immediate and universal, and practical life becomes the work of closing the gap between that recognition and ordinary decisions about meals, textiles, cosmetics, travel, sport, media, and nightlife when those routes still treat other animals as resources.
 
-If you want recipes and tips, start with small changes.
-Going vegan is a journey, and you can celebrate each win along the way.
+Recipes, clothing swaps, and travel tips can be useful once the recognition leads.
+They describe how the principle shows up in life; they are not what the principle is.
+Keep the steps practical, keep the argument structural, and keep the demand universal.
```

To regenerate a similar diff locally after editing two files:

`diff -u example-before.txt example-after.txt`

---

## What this sample is testing

- **Misframing removed:** “lifestyle,” “reduce cruelty,” “plant-based” as stand-in for principle, “minimise harm,” consumer-only leverage, gradualism as moral permission, journey framing.
- **Structural claim landed:** exploitation named as use and ownership, not only bad feelings; calm-cow counterexample for painless exploitation.
- **Welfare exit closed:** humane and free-range reframed as negotiation inside injustice, not a solution.
- **Compassion reframed:** valid entry, not the foundation of obligation.
- **Reader accountability:** concrete domains (meals, textiles, cosmetics, travel, sport, media, nightlife) without reducing the wrong to shopping alone.
- **Output constraint:** no em dashes in the replacement passage (per `AGENT_INSTRUCTIONS.md`).

Replace the synthetic article with a real ADAPTT page when you run an actual pass.

For the same layout with **strong language** kept on purpose, see [`EXAMPLE_REWRITE_OUTPUT_VULGAR.md`](EXAMPLE_REWRITE_OUTPUT_VULGAR.md).
