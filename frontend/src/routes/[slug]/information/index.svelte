<script>
	import { module, app } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';
	import { Marked } from '$lib/macro';
	import { Card } from '$lib/layout';

	let { item, edit_mode, update } = $props();
	let open = $state(false);
</script>

<div class="margin">
	{#if app.user.access.includes('item:edit_information') && edit_mode}
		<Edit_Button
			onclick={() =>
				module.open(Form, {
					key: item.key,
					information: item.information,
					update
				})}>Edit information</Edit_Button
		>
	{/if}

	{#if item.information}
		<Card {open} onopen={() => (open = !open)}>
			{#snippet title()}
				Details & Specifications
			{/snippet}
			<Marked content={item.information}></Marked>
		</Card>
	{:else if edit_mode}
		No information
	{/if}
</div>

<style>
	.margin {
		margin: var(--sp2) 0;
	}
</style>
