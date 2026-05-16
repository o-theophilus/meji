<script>
	import { app, module } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';

	let { item, edit_mode, update } = $props();
	let edit = $derived(app.user.access.includes('item.edit_metadata') && edit_mode);
</script>

<div class="area" class:edit>
	{#if edit}
		<Edit_Button
			onclick={() =>
				module.open(Form, {
					key: item.key,
					length: item.metadata.length,
					breadth: item.metadata.breadth,
					height: item.metadata.height,
					weight: item.metadata.weight,
					address: item.metadata.address,
					area: item.metadata.area,
					prep_time: item.metadata.prep_time,
					update
				})}
		>
			Edit Metadata
		</Edit_Button>
		<div class="title">Metadata</div>

		<div class="details">
			<span class="label">Length</span> <span>{item.metadata.length}cm</span>
			<span class="label">Breadth</span> <span>{item.metadata.breadth}cm</span>
			<span class="label">Height</span> <span>{item.metadata.height}cm</span>
			<span class="label">Weight</span> <span>{item.metadata.weight}kg</span>
			<span class="label">Address</span> <span>{item.metadata.address}</span>
			<span class="label">Area</span> <span>{item.metadata.area}</span>
			<span class="label">Prep Time</span> <span>{item.metadata.prep_time} days</span>
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
