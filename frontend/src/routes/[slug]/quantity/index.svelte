<script>
	import { app, module } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';

	let { item, edit_mode, update } = $props();
	let edit = $derived(app.user.access.includes('item.edit_quantity') && edit_mode);
</script>

<div class="area" class:edit>
	{#if edit}
		<Edit_Button
			onclick={() =>
				module.open(Form, {
					key: item.key,
					quantity: item.quantity,
					update
				})}
		>
			Edit Quantity
		</Edit_Button>
		<div class="page_title">
			{item.quantity}
		</div>
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
