<script>
	import { slide } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	import { currency } from '$lib/store.js';

	import Button from '$lib/comp/button.svelte';

	export let item = {};
	let show_details = false;
</script>

<div class="cost">
	<div class="price">
		{currency(item.price)}
	</div>
	{#if item.old_price}
		<div class="old_price">
			{currency(item.old_price)}
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
		<div>{currency(item.old_price)}</div>

		<div>Selling Price</div>
		<div>{currency(item.price)}</div>

		<div>Discount</div>
		<div>{(((item.old_price - item.price) * 100) / item.old_price).toFixed(0)}% off</div>

		<div class="hr" />

		<div>Total</div>
		<div>{currency(item.price)}</div>

		<div class="hr" />

		<div>Overall save</div>
		<div>{currency(item.old_price - item.price)}</div>
	</dir>
{/if}

<style>
	.cost {
		display: flex;
		flex-wrap: wrap;

		align-items: center;
		gap: var(--gap2);
	}
	.price {
		font-weight: 500;
		font-size: 1.2rem;
		color: var(--color3);
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
		background: var(--color4);
	}
	.discount {
		color: var(--midtone);
	}

	.details {
		display: grid;
		gap: var(--gap1) var(--gap3);
		grid-template-columns: 1fr auto;

		padding: var(--gap2);
		background-color: var(--background);
		border-radius: var(--gap1);

		font-size: x-small;
		width: 100%;
	}
	.hr {
		grid-column: 1/3;
		height: 2px;
		background-color: var(--midtone);
	}
</style>
