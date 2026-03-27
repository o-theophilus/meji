<script>
	import { Icon } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';
	import Info from './info.svelte';

	let { item, edit_mode, update, children } = $props();
	let edit = $derived(app.user.access.includes('item.edit_price') && edit_mode);
</script>

<div class="line space">
	<div class="area" class:edit>
		{#if edit}
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

<style>
	.area {
		margin-top: 8px;
		&.edit {
			padding: 8px;
			border-radius: 4px;
			outline: 1px solid var(--ol);
			outline-offset: -1px;
		}
	}

	.price {
		font-weight: 700;
		font-size: 1.8rem;
		color: var(--ft1);

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
