<script>
	import { module, app, page_state } from '$lib/store.svelte.js';
	import { goto } from '$app/navigation';

	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';
	import { Card } from '$lib/layout';
	import Value from './value.svelte';

	let { item, edit_mode, update } = $props();
	let open = $state(true);
</script>

{#if Object.keys(item.variation).length != 0}
	<Card
		{open}
		onclick={() => (open = !open)}
		--card-bottom-border-color="var(--bg1)"
		--card-title-padding="16px 0"
		--card-content-padding="0"
	>
		{#snippet title()}
			{#if app.user.access.includes('item:edit_variation') && edit_mode}
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

		<div class="grid">
			{#each Object.entries(item.variation) as [key, values]}
				<div class="key">
					{key}:
				</div>

				<div class="line">
					{#each values as value}
						<Value {value}></Value>
					{/each}
				</div>
			{/each}
		</div>
	</Card>
{:else if edit_mode}
	No Variation
{/if}

<style>
	.title {
		font-weight: 800;
	}

	.grid {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 16px;
		align-items: center;

		margin: 24px 0;
	}

	.key {
		text-transform: capitalize;
	}
</style>
