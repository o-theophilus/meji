<script>
	import { module, loading, notify, app, page_state } from '$lib/store.svelte.js';
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
	import { Note } from '$lib/info';
	import Value from '../../[slug]/variation/value.svelte';
	import Form from './form.svelte';

	let { item, ops } = $props();

	let error = $derived.by(() => {
		if (item.status != 'active') {
			return 'This item is not currently available';
		} else if (item.available_quantity == 0) {
			return 'Sorry, this item is currently out of stock';
		} else if (item.quantity > item.available_quantity) {
			return `Only ${item.available_quantity} item${item.available_quantity > 1 ? 's' : ''} available in stock`;
		}
		return null;
	});

	const remove = async () => {
		app.cart_items = app.cart_items.filter(
			(x) => !(x.key == item.key && JSON.stringify(x.variation) == JSON.stringify(item.variation))
		);

		loading.open('Removing item from cart . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ key: item.key, variation: item.variation })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.cart_items = resp.items;
			notify.open('Item removed from cart');
			page_state.clear('cart');
		} else {
			error = resp;
		}
	};
</script>

<!-- TODO: indicate items that are not active or quantity == 0 
	set restriction on quantity to avoid unessary quantity set
-->

<div class="item">
	<div class="block">
		<a class="img" href="/{item.slug}">
			<img
				src="{item.photo}/500"
				loading="lazy"
				alt={item.name}
				onerror={(e) => (e.target.src = '/no_photo.png')}
			/>
		</a>

		<div class="details">
			<div class="name_quantity">
				<div>
					<a class="name" href="/{item.slug}">
						{item.name}
					</a>
					<div class="variation">
						{#each Object.entries(item.variation) as [key, value], i}
							{#if i != 0},{/if}
							{key}: <Value {value} small></Value>
						{/each}
					</div>
				</div>
				<div class="line">
					<Button onclick={() => module.open(Form, { item, ops })}>Qty</Button>
					<Button icon="trash2" onclick={remove}></Button>
				</div>
			</div>

			<div class="line space">
				<span>
					<span class="price">
						{#if item.price}
							₦{Number(item.price).toLocaleString()}
						{/if}
					</span>
					x {item.quantity}
				</span>

				<div class="total">
					₦{(item.price * item.quantity).toLocaleString()}
				</div>
			</div>
		</div>
	</div>
	<Note note={error} status="100" --note-margin-top="16px" --note-margin-bottom="0"></Note>
</div>

<style>
	.item {
		padding: 16px;
		border-radius: 8px;
		background-color: var(--bg3);
		outline: 1px solid var(--ol);
		outline-offset: -2px;
	}

	.block {
		display: flex;
		gap: 16px;
	}

	.img {
		display: flex;
		width: 120px;
		height: 120px;
		flex-shrink: 0;
	}

	img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		border-radius: 4px;
		line-height: 100%;

		outline: 2px solid transparent;
		outline-offset: 2px;
		transition: outline-color var(--trans);
	}

	a:hover img {
		outline-color: var(--ft1);
	}

	.details {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 16px;

		width: 100%;
	}
	.name_quantity {
		display: flex;
		gap: 8px;
		justify-content: space-between;
	}

	.name {
		display: block;
		text-decoration: none;
		color: var(--ft2);
	}

	.variation {
		font-size: 0.8rem;
	}

	.total {
		font-weight: 700;
		color: var(--ft1);
	}
</style>
