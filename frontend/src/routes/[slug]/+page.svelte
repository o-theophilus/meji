<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { module, app, page_state } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { Button, Toggle } from '$lib/button';
	import { Meta, Log, ToTop } from '$lib/macro';
	import Edit_Button from './edit_button.svelte';

	import {
		Status,
		Photo,
		Date,
		Name,
		Tags,
		Price,
		Information,
		Quantity,
		Review,
		Variation
	} from '.';
	import Highlight from './highlight.svelte';
	import Similar from './similar.svelte';

	import Like from '../shop/like.svelte';
	import Share from './share.svelte';
	import AddCart from '../cart/add_to_cart.svelte';

	let { data } = $props();
	let item = $derived(data.item);
	let review = $state({});
	let item_group = $state([]);
	let edit_mode = $state(false);
	let loading = $state(false);
	let is_admin = app.user.access.some((x) =>
		[
			'item:add',
			'item:edit_status',
			'item:edit_file',
			'item:edit_date',
			'item:edit_name',
			'item:edit_tag',
			'item:edit_price',
			'item:edit_information',
			'item:edit_files',
			'item:edit_variation',
			'item:edit_quantity',
			'item:edit_highlight',
			'item:advert'
		].includes(x)
	);

	const update = (data) => {
		item = data;
		page_state.clear('home');
		page_state.clear('shop');
		page_state.clear('save');
		page_state.clear('cart');
	};

	const refresh = async (data) => {
		item = data;
		loading = true;

		if (page.url.searchParams.has('edit') && is_admin) {
			page.url.searchParams.delete('edit');
			edit_mode = true;
			window.history.replaceState(history.state, '', page.url.href);
		} else {
			edit_mode = false;
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item_group/${item.key}`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();

		if (resp.status == 200) {
			review = resp.review;
			item_group = resp.item_group;
		}
		loading = false;
	};

	onMount(async () => refresh(item));
</script>

{#key item.key}
	<Log action={'viewed'} entity_key={item.key} entity_type={'item'} />
{/key}

<Meta
	title={item.name}
	description={item.information.length > 100
		? item.information.slice(0, 100) + '...'
		: item.information}
	image={item.photo}
/>

<Content --content-background-color="var(--bg)" --content-padding-bottom="0">
	{#if is_admin}
		<Toggle state_2="edit" active={edit_mode} onclick={() => (edit_mode = !edit_mode)} />
		<br />
	{/if}

	{#if edit_mode && (app.user.access.includes('item:edit_status') || app.user.access.includes('item:edit_highlight'))}
		<div class="line status">
			<Status {item} {update}></Status>
			<Highlight {item} />
		</div>
	{/if}

	<div class="photo_info">
		<div class="photo">
			<Photo bind:item {edit_mode} {update} />
		</div>

		<div class="info">
			<Date {item} {edit_mode} {update} />
			<Name {item} {edit_mode} {update} />
			<Tags {item} {edit_mode} {update} />
			<Price {item} {edit_mode} {update} />
			<Information {item} {edit_mode} {update} />
			<Variation {item} {edit_mode} {update} />
			<Quantity {item} {edit_mode} {update} />
			<Review {item} {review} {loading} />
		</div>
	</div>
</Content>

<div class="floater">
	<div class="floater_block">
		{#if item.status == 'active' && item.quantity > 0}
			<Button
				--button-background-color="var(--cl1)"
				--button-background-color-hover="color-mix(in srgb, var(--cl1), black 50%)"
				--button-color="hsl(0, 0%, 95%)"
				--button-color-hover="hsl(0, 0%, 95%)"
				icon="cart"
				onclick={() => module.open(AddCart, item)}>Add to Chat</Button
			>
		{:else}
			<Button
				--button-background-color="color-mix(in srgb, red, transparent 80%)"
				--button-outline-color="red"
				--button-color="hsl(0, 0%, 95%)"
			>
				{#if item.status != 'active'}
					Unavailable
				{:else if item.quantity == 0}
					Out of stock
				{/if}
			</Button>
		{/if}

		<Button
			icon="whatsapp"
			href="https://api.whatsapp.com/send?phone=+2349113717298&text=Hi%0AI want to make enquiry concerning ${item.name} on Meji.ng%20{page
				.url.href}"
			target="_blank"
		>
			Chat
		</Button>

		<Like {item} />

		<Button icon="share-2" onclick={() => module.open(Share, item)}></Button>
	</div>
</div>

<Content
	--content-height
	--content-padding-top="0"
	--content-padding-bottom="0"
	--content-background-color="var(--bg)"
>
	{#each item_group as group}
		<Similar {group} {refresh} {loading} />
	{/each}
	<!-- TODO: <ToTop /> -->
</Content>

<style>
	.photo_info {
		display: flex;
		flex-direction: column;
		gap: 24px;
	}
	.info {
		margin-top: 24px;
	}

	.photo,
	.info {
		width: 100%;
	}

	.floater {
		position: sticky;
		bottom: var(--headerHeight2);

		background-color: var(--bg);
		border-top: 1px solid var(--ol);
	}

	.floater_block {
		display: flex;
		gap: 4px;
		flex-wrap: wrap;

		padding: 8px 24px;
		max-width: var(--mobileWidth);
		margin: auto;
	}

	@media screen and (min-width: 800px) {
		.photo_info {
			flex-direction: unset;
			position: relative;
		}

		.photo {
			position: sticky;
			top: 16px;

			align-self: flex-start;
		}

		.info {
			margin: 0;
		}
	}

	.line.status {
		margin-bottom: 8px;
	}
</style>
