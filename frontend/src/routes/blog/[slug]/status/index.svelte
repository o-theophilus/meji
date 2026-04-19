<script>
	import { app, module } from '$lib/store.svelte.js';

	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { blog, edit_mode, update } = $props();
</script>

{#if edit_mode && app.user.access.includes('blog.edit_status')}
	<div class="block">
		<Button
			onclick={() =>
				module.open(Edit, {
					key: blog.key,
					status: blog.status,
					photo: blog.photo,
					update
				})}
		>
			Edit Status: <span class="status {blog.status}">{blog.status}</span>
		</Button>
	</div>
{/if}

<style>
	.block {
		margin-bottom: 8px;
	}
	.status {
		font-weight: 800;
	}
	.status.active {
		color: green;
	}
	.status.draft {
		color: red;
	}
</style>
