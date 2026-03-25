<script>
	import { app, module, page_state } from '$lib/store.svelte.js';

	import { Tag } from '$lib/button';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { blog, edit_mode, update } = $props();
	let edit = $derived(app.user.access.includes('blog.edit_tags') && edit_mode);
</script>

<div class="area" class:edit>
	{#if edit}
		<Button
			onclick={() =>
				module.open(Edit, {
					key: blog.key,
					title: blog.title,
					tags: blog.tags,
					update
				})}>Edit Tags</Button
		>
	{/if}

	{#if blog.tags.length > 0}
		<div class="line">
			{#each blog.tags as x}
				<Tag onclick={() => page_state.goto('blog', { tag: x })}>
					{x}
				</Tag>
			{/each}
		</div>
	{:else if edit_mode}
		<div class="notag">No tag</div>
	{/if}
</div>

<style>
	.area {
		margin-top: 8px;
		&.edit {
			padding: 8px;
			border-radius: 4px;
			outline: 1px solid var(--ol);
			outline-offset: -1px;
		}
	}

	.notag {
		font-size: 0.8rem;
	}

	.line {
		margin-top: 8px;
		gap: 4px;
	}
</style>
