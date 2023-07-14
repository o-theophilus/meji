<script>
	import { slide } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	import Button from '$lib/button.svelte';

	export let item;
	let show_details = false;
</script>

<div class="cost">
	<div class="price">
		{#if item.price}
			₦{item.price.toLocaleString()}
		{:else}
			Nil
		{/if}
	</div>
	{#if item.old_price}
		<div class="old_price">
			₦{item.old_price.toLocaleString()}
			<div class="strike" />
		</div>
		<div class="discount">
			{(((item.old_price - item.price) * 100) / item.old_price).toFixed(0)}% off
		</div>
		<Button
			icon="info"
			class="tiny"
			icon_size="8"
			on:click={() => {
				show_details = !show_details;
			}}
		/>
	{/if}
</div>

{#if show_details}
	<dir class="details" transition:slide|local={{ delay: 0, duration: 200, easing: quintOut }}>
		<div>Maximum Price</div>
		<div>₦{item.old_price.toLocaleString()}</div>

		<div>Selling Price</div>
		<div>₦{item.price.toLocaleString()}</div>

		<div>Discount</div>
		<div>{(((item.old_price - item.price) * 100) / item.old_price).toFixed(0)}% off</div>

		<div class="hr" />

		<div>Total</div>
		<div>₦{item.price.toLocaleString()}</div>

		<div class="hr" />

		<div>Overall save</div>
		<div>₦{(item.old_price - item.price).toLocaleString()}</div>
	</dir>
{/if}

<style>
	.cost {
		display: flex;
		flex-wrap: wrap;

		align-items: center;
		gap: var(--sp2);
	}
	.price {
		font-weight: 500;
		font-size: 1.2rem;
		color: var(--cl3);
	}

	.old_price {
		position: relative;
		color: var(--midtone);
	}
	.strike {
		position: absolute;
		top: calc(50% - 0.5px);
		left: -3px;
		right: -3px;

		height: 1px;

		transform: rotate(-10deg);
		background: var(--cl4);
	}
	.discount {
		color: var(--midtone);
	}

	.details {
		display: grid;
		gap: var(--sp1) var(--sp3);
		grid-template-columns: 1fr auto;

		padding: var(--sp2);
		background-color: var(--ac5);
		border-radius: var(--sp1);

		font-size: x-small;
		width: 100%;
	}
	.hr {
		grid-column: 1/3;
		height: 2px;
		background-color: var(--midtone);
	}
</style>
