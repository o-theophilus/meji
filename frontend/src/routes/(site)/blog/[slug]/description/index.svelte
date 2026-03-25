<script>
	import { app, module } from '$lib/store.svelte.js';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { blog, edit_mode, update } = $props();
</script>

<div class="margin">
	{#if app.user.access.includes('blog.edit_description') && edit_mode}
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
	.margin {
		margin: 16px 0;
	}
</style>
