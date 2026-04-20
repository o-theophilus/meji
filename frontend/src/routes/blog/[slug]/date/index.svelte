<script>
	import { app, module } from '$lib/store.svelte.js';

	import { Datetime } from '$lib/macro';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { blog, edit_mode, update } = $props();
	let edit = $derived(app.user.access.includes('blog.edit_date') && edit_mode);
</script>

<div class="area" class:edit>
	{#if edit}
		<Button
			onclick={() =>
				module.open(Edit, {
					key: blog.key,
					date_created: blog.date_created,
					update
				})}
		>
			Edit Date
		</Button>
	{/if}

	<div class="date">
		<Datetime datetime={blog.date_created} />
	</div>
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
	.date {
		font-size: 0.8rem;
	}
</style>
