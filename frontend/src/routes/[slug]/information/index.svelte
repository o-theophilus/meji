<script>
	import { module, app } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';
	import { Marked } from '$lib/macro';
	import { Card } from '$lib/layout';

	let { item, edit_mode, update } = $props();
	let open = $state(true);
</script>

{#if item.information}
	<Card
		{open}
		onclick={() => (open = !open)}
		--card-bottom-border-color="var(--bg1)"
		--card-title-padding="16px 0"
		--card-content-padding="0"
	>
		{#snippet title()}
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
			<div class="title">Details & Specifications</div>
		{/snippet}
		<Marked content={item.information}></Marked>
	</Card>
{:else if edit_mode}
	No information
{/if}

<style>
	.title {
		font-weight: 800;
	}
</style>
