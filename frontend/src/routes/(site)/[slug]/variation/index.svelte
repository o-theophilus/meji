<script>
	import { Card } from '$lib/layout';
	import { app, module } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';
	import Value from './value.svelte';

	let { item, edit_mode, update } = $props();
	let open = $state(true);
	let edit = $derived(app.user.access.includes('item.edit_variation') && edit_mode);
</script>

{#if Object.keys(item.variation).length || edit}
	<div class="hr"></div>
	<Card
		{open}
		onclick={() => (open = !open)}
		--card-title-padding="0"
		--card-content-padding="16px 0"
	>
		{#snippet title()}
			{#if edit}
				<Edit_Button
					onclick={() =>
						module.open(Form, {
							key: item.key,
							name: item.name,
							variation: item.variation,
							update
						})}
					>Edit Variation
				</Edit_Button>
			{/if}
			<div class="title">
				Variation{#if Object.keys(item.variation).length > 1}s{/if}
			</div>
		{/snippet}

		{#if Object.keys(item.variation).length}
			<div class="grid">
				{#each Object.entries(item.variation) as [key, values]}
					<div class="key">
						{key}
					</div>

					<div class="line">
						{#each values as value}
							<Value {value}></Value>
						{/each}
					</div>
				{/each}
			</div>
		{:else}
			No Variation
		{/if}
	</Card>
{/if}

<style>
	.hr {
		margin-top: 16px;
		background-color: var(--ft1);
		height: 1px;
	}

	.title {
		font-weight: 800;
		color: var(--ft1);
	}

	.grid {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 16px;
		align-items: center;
	}

	.key {
		text-transform: capitalize;
		font-size: 0.8rem;
	}
</style>
