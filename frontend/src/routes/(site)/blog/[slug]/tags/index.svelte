<script>
	import { app, module, page_state } from '$lib/store.svelte.js';

	import { Tag } from '$lib/button';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { blog, edit_mode, update } = $props();
</script>

{#if blog.tags.length > 0 || (app.user.access.includes('blog.edit_tags') && edit_mode)}
	<hr />
{/if}

{#if app.user.access.includes('blog.edit_tags') && edit_mode}
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

<style>
	.notag {
		font-size: 0.8rem;
	}

	.line {
		margin-top: 8px;
		gap: 4px;
	}
</style>
