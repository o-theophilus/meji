<script>
	import { app, module } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';

	let { item, edit_mode, update } = $props();
	let edit = $derived(app.user.access.includes('item.edit_package') && edit_mode);
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
			Edit Package
		</Edit_Button>
		<div class="title">Package</div>

		<div class="details">
			<span class="label">Length</span> <span>{item.package.length}cm</span>
			<span class="label">Breadth</span> <span>{item.package.breadth}cm</span>
			<span class="label">Height</span> <span>{item.package.height}cm</span>
			<span class="label">Weight</span> <span>{item.package.weight}kg</span>
			<span class="label">Address</span> <span>{item.package.address}</span>
			<span class="label">Area</span> <span>{item.package.area}</span>
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

	.title {
		font-weight: 800;
		color: var(--ft1);
	}

	.details {
		display: grid;
		grid-template-columns: repeat(2, max-content);
		gap: 0 16px;
		margin-top: 8px;
	}
</style>
