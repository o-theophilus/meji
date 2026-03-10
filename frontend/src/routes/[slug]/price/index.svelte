<script>
	import { Icon } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';
	import Info from './info.svelte';

	let { item, edit_mode, update, children } = $props();

	let show_discount = $state(false);
</script>

<div class="comp">
	{#if app.user.access.includes('item.edit_price') && edit_mode}
		<Edit_Button
			onclick={() =>
				module.open(Form, {
					key: item.key,
					price: item.price,
					price_old: item.price_old,
					update
				})}
		>
			Edit Price
		</Edit_Button>
	{/if}

	<div class="line space">
		<div>
			<div class="price">
				{#if Number(item.price)}
					₦{Number(item.price).toLocaleString()}
				{:else}
					<span> Nil </span>
				{/if}
			</div>

			{#if Number(item.price_old)}
				<div class="line">
					<span class="old_price">
						₦{Number(item.price_old).toLocaleString()}
						<div class="strike"></div>
					</span>

					<button onclick={() => module.open(Info, { item })}>
						<Icon icon="info"></Icon>
					</button>
				</div>
			{/if}
		</div>

		{@render children?.()}
	</div>

	<!-- {#if show_discount}
		<div transition:slide>
			<Info {item}></Info>
		</div>
	{/if} -->
</div>

<style>
	.comp {
		margin-top: 24px;
	}

	.price {
		font-weight: 700;
		font-size: xx-large;
		color: var(--ac1);

		span {
			color: red;
		}
	}

	.old_price {
		position: relative;

		.strike {
			position: absolute;
			top: calc(50% - 0.5px);
			left: -3px;
			right: -3px;

			height: 2px;

			transform: rotate(-10deg);
			background: red;
		}
	}

	button {
		all: unset;
		cursor: pointer;

		display: flex;
		transition: color 0.2s ease-in-out;

		&:hover {
			color: var(--ft1);
		}
	}
</style>
