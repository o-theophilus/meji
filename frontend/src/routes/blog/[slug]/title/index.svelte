<script>
	import { app, module } from '$lib/store.svelte.js';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { blog, edit_mode, update } = $props();
	let edit = $derived(app.user.access.includes('blog.edit_title') && edit_mode);
</script>

<div class="area" class:edit>
	{#if edit}
		<Button
			onclick={() =>
				module.open(Edit, {
					key: blog.key,
					title: blog.title,
					update
				})}
		>
			Edit Title
		</Button>
	{/if}

	<div class="page_title">
		{blog.title}
	</div>
</div>

<style>
	.area {
		margin-top: 16px;
		&.edit {
			padding: 8px;
			border-radius: 4px;
			outline: 1px solid var(--ol);
			outline-offset: -1px;
		}
	}
</style>
