<script>
	import { RoundButton } from '$lib/button';
	import Value from './value.svelte';

	let { ops = $bindable() } = $props();
</script>

<div class="title">
	Variation{#if Object.keys(ops.variation).length > 1}s{/if}
</div>

<div class="grid">
	{#each Object.entries(ops.variation) as [key, values]}
		<div class="key">
			{key}:
		</div>

		<div class="line">
			{#each values as value (key + value + Math.random())}
				<Value {value}></Value>
			{/each}
		</div>

		<div class="control">
			<RoundButton
				icon="square-pen"
				onclick={() => {
					ops.key = key;
					ops.value = values.join(', ');
					ops.error = {};
				}}
			/>

			<RoundButton
				icon="trash-2"
				--button-background-color-hover="red"
				onclick={() => {
					delete ops.variation[key];
					ops.error = {};
				}}
			/>
		</div>
	{:else}
		No Variation
	{/each}
</div>

<style>
	.title {
		font-size: large;
		font-weight: 800;
		color: var(--ft1);
		margin: 16px 0;
	}

	.grid {
		display: grid;
		grid-template-columns: auto 1fr auto;
		gap: 8px 16px;
		gap: 16px;
		align-items: center;

		margin: 16px 0;
	}

	.key {
		text-transform: capitalize;
	}
</style>
