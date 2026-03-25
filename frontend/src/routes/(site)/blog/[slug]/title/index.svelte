<script>
	import { app, module } from '$lib/store.svelte.js';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { blog, edit_mode, update } = $props();
</script>

<div class="comp">
	{#if app.user.access.includes('blog.edit_title') && edit_mode}
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
	.comp {
		margin-top: 24px;
	}
</style>
