import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const findings = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/findings" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.string(),
    round: z.string().optional(),
    scope: z.enum(["round", "synthesis"]),
    trials: z.number(),
    models: z.number(),
    headline: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const experiments = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/experiments" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    status: z.enum(["active", "complete", "planned"]),
    rounds: z.number(),
    totalTrials: z.number(),
  }),
});

export const collections = { findings, experiments };
