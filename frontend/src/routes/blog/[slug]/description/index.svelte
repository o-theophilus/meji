<script>
	import { app, module } from '$lib/store.svelte.js';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { blog, edit_mode, update } = $props();
	let edit = $derived(app.user.access.includes('blog.edit_description') && edit_mode);
</script>

<div class="area" class:edit>
	{#if edit}
		<Button
			onclick={() =>
				module.open(Edit, {
					key: blog.key,
					description: blog.description,
					update
				})}>Edit Description</Button
		>
	{/if}

	{#if blog.description}
		{blog.description}
	{:else if edit_mode}
		No description
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
</style>
