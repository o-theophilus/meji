<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { user, module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
	import Value from '$lib/item/variation_value.svelte';
	import Form from './variation_form.svelte';

	export let item = {};
	export let edit_mode = false;
	let open = Object.keys(item.variation).length > 0;
</script>

{#if edit_mode || Object.keys(item.variation).length > 0}
	<div class="row space v_margin">
		<span class="bold">
			Variation{Object.keys(item.variation).length > 1 ? 's' : ''}
		</span>
		<div class="row">
			<ButtonFold
				{open}
				on:click={() => {
					open = !open;
				}}
			/>
			{#if edit_mode && $user.permissions.includes('item:edit_variation')}
				<BRound
					icon="edit"
					icon_size="10"
					tooltip="Edit Variation"
					on:click={() => {
						$module = {
							module: Form,
							item
						};
					}}
				/>
			{/if}
		</div>
	</div>

	{#if open}
		<div class="v_margin" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each Object.entries(item.variation) as [key, values]}
				{@const s = values.length > 0 ? 's' : ''}
				<div class="property">
					<span>{key}{s}: &nbsp;</span>

					{#each values as value, i}
						{#if i != 0}, &nbsp; {/if}
						<Value {value} />
					{/each}
				</div>
			{:else}
				No Variation
			{/each}
		</div>
	{/if}
{/if}

<style>
	.row {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.space {
		justify-content: space-between;
	}

	.v_margin {
		margin: var(--sp1) 0;
	}

	.bold {
		color: var(--ac1);
		text-transform: capitalize;
		font-weight: 700;
	}

	.property {
		display: flex;
		flex-wrap: wrap;
		align-items: end;
	}
</style>
