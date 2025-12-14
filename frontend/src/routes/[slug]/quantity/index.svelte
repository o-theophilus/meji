<script>
	import { module, app } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import { Button } from '$lib/button';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';

	let { item, edit_mode, update } = $props();
</script>

<div class="comp">
	{#if app.user.access.includes('item:edit_quantity') && edit_mode}
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
	{/if}
	<div class="page_title">
		{item.quantity}
	</div>
</div>

<style>
	.comp {
		margin-top: var(--sp3);
	}
</style>
