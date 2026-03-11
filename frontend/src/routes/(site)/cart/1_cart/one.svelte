<script>
	import { Button, RoundButton } from '$lib/button';
	import { Note } from '$lib/info';
	import { Input } from '$lib/input';
	import { app, notify, page_state } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import Value from './variation_value.svelte';

	let { item, ops } = $props();
	let open_menu = $state(false);
	let self = $state(false);
	let error = $state({});

	let error_note = $derived.by(() => {
		if (item.status != 'active') {
			return 'This item is not currently available';
		} else if (item.available_quantity == 0) {
			return 'Sorry, this item is currently out of stock';
		} else if (item.quantity >= item.available_quantity) {
			return `Only ${item.available_quantity} item${item.available_quantity > 1 ? 's' : ''} available in stock`;
		}
		return null;
	});

	const remove = async () => {
		ops.error = {};

		app.cart_items = app.cart_items.filter(
			(x) => !(x.key == item.key && JSON.stringify(x.variation) == JSON.stringify(item.variation))
		);

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ key: item.key, variation: item.variation })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			app.cart_items = resp.items;
			notify.open('Item removed from cart');
			page_state.clear('cart');
		} else {
			error = resp;
		}
	};

	const validate = () => {
		ops.error = {};
		error = {};

		if (item.quantity && (!Number.isInteger(item.quantity) || item.quantity < 1)) {
			error.quantity = 'Please enter a valid number';
		} else if (item.quantity > item.available_quantity) {
			error.quantity = `Only ${item.available_quantity} items available in stock`;
		}

		Object.keys(error).length === 0 && submit();
	};

	let timeout;
	const submit = () => {
		clearTimeout(timeout);
		timeout = setTimeout(async () => {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart/quantity`, {
				method: 'post',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify({
					key: item.key,
					quantity: item.quantity,
					variation: item.variation
				})
			});
			resp = await resp.json();

			if (resp.status == 200) {
				app.cart_items = resp.items;
				page_state.clear('cart');
			} else {
				error = resp;
			}
		}, 1000);
	};
</script>

<svelte:window
	onclick={() => {
		if (open_menu && !self) {
			open_menu = false;
		}
		self = false;
	}}
/>

<div class="container">
	<div class="block">
		<svelte:element this={item.status == 'active' ? 'a' : 'span'} class="img" href="/{item.slug}">
			<img
				src="{item.photo}/500"
				loading="lazy"
				alt={item.name}
				onerror={(e) => (e.target.src = '/no_photo.png')}
			/>
		</svelte:element>

		<div class="details">
			<div class="row_1">
				<div>
					<svelte:element
						this={item.status == 'active' ? 'a' : 'span'}
						class="name"
						href="/{item.slug}"
					>
						{item.name}
					</svelte:element>
					<div class="variation">
						{#each Object.entries(item.variation) as [key, value], i}
							{#if i != 0},{/if}
							{key}: <Value {value}></Value>
						{/each}
					</div>
				</div>

				<div class="menu_area">
					<RoundButton
						icon={open_menu ? 'x' : 'ellipsis'}
						onclick={() => {
							open_menu = !open_menu;
							self = true;
						}}
					></RoundButton>
					{#if open_menu}
						<div class="menu" transition:slide={{ axis: 'x' }}>
							<Button icon="trash2" icon_size="12" onclick={remove}>Remove</Button>
						</div>
					{/if}
				</div>
			</div>

			<div class="line space">
				<div class="line">
					<span class="price">
						{#if item.price}
							₦{Number(item.price).toLocaleString()}
						{/if}
					</span>
					x
					<Input
						--number-height="24px"
						--number-width="24px"
						--button-padding-x="0"
						--number-pading-x="0"
						--input-min-width="40px"
						type="number"
						value={item.quantity}
						min={1}
						max={item.available_quantity}
						ondone={(e) => {
							app.cart_items = app.cart_items.map((x) => {
								if (
									x.key == item.key &&
									JSON.stringify(x.variation) == JSON.stringify(item.variation)
								) {
									return { ...x, quantity: e };
								}
								return x;
							});
							item.quantity != e && validate();
						}}
					></Input>
				</div>

				<div class="total">
					₦{(item.price * item.quantity).toLocaleString()}
				</div>
			</div>
		</div>
	</div>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<Note note={error_note} status="100" --note-margin-top="16px" --note-margin-bottom="0"></Note>
</div>

<style>
	.container {
		padding: 16px;
		border-radius: 8px;
		background-color: var(--bg3);
		outline: 1px solid var(--ol);
		outline-offset: -1px;

		& .block {
			display: flex;
			gap: 16px;
		}

		&:has(a:hover) img {
			outline-color: var(--ft1);
		}
	}

	.img {
		display: flex;
		width: 80px;
		height: 80px;
		flex-shrink: 0;

		& img {
			width: 100%;
			height: 100%;
			object-fit: cover;
			border-radius: 4px;
			line-height: 100%;

			outline: 2px solid transparent;
			outline-offset: 2px;
			transition: outline-color 0.2s ease-in-out;
		}
	}

	.details {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 16px;

		width: 100%;

		& .row_1 {
			display: flex;
			gap: 8px;
			justify-content: space-between;

			& .name {
				display: block;
				text-decoration: none;
				color: var(--ft1);
			}

			& .variation {
				font-size: 0.8rem;
			}
		}
	}

	.total {
		font-weight: 700;
		color: var(--ft1);
	}

	.menu_area {
		position: relative;

		& .menu {
			position: absolute;
			top: 0;
			right: 36px;

			display: flex;
			flex-direction: column;
			gap: 1px;

			--button-font-size: 0.7rem;
			--button-height: 32px;
			--button-width: 100%;
			--button-padding-x: 12px;
		}
	}

	.error {
		margin-top: 8px;
		color: red;
		font-size: 0.8rem;
	}
</style>
