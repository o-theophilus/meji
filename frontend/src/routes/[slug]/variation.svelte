<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { user, module } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import SVG from '$lib/svg.svelte';
	import Value from '$lib/item/variation_value.svelte';
	import Form from './variation_form.svelte';

	export let item = {};
	export let edit_mode = false;
	let open = Object.keys(item.variation).length > 0;
</script>

{#if edit_mode || Object.keys(item.variation).length > 0}
	<div class="horizontal bold">
		Variation{Object.keys(item.variation).length > 1 ? 's' : ''}
		<div class="horizontal">
			<ButtonFold
				{open}
				on:click={() => {
					open = !open;
				}}
			/>
			{#if edit_mode && $user.permissions.includes('item:edit_variation')}
				<Button
					class="round"
					on:click={() => {
						$module = {
							module: Form,
							item
						};
					}}
					tooltip="Edit Variation"
				>
					<SVG type="edit" size="10" />
				</Button>
			{/if}
		</div>
	</div>
	{#if open}
		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
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
	.horizontal {
		display: flex;
		justify-content: space-between;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
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
