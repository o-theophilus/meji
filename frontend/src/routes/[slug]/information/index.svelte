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
	<br />
	<Card
		{open}
		onclick={() => (open = !open)}
		--card-title-padding="0"
		--card-content-padding="16px 0"
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
			<div class="title">
				Details & Specifications
				<div class="hr"></div>
			</div>
		{/snippet}
		<Marked content={item.information}></Marked>
	</Card>
{:else if edit_mode}
	No information
{/if}

<style>
	.title {
		display: flex;
		align-items: center;
		gap: 16px;

		font-weight: 800;
		color: var(--ft1);

		& .hr {
			background-color: var(--ft1);
			height: 2px;
			flex-grow: 1;
		}
	}
</style>
