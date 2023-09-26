<script>
	import { slide } from 'svelte/transition';
	import { elasticInOut } from 'svelte/easing';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { user, module, loading } from '$lib/store.js';
	import { onMount } from 'svelte';

	import Button from '$lib/button.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import SVG from '$lib/svg.svelte';
	import Price from './info.price.svelte';
	import Discount from './info.price.discount.svelte';
	import Rating from '$lib/item/rating.svelte';
	import Review from './feedback/review.svelte';
	import Save from '$lib/item/save.svelte';
	import Add_Cart from '$lib/item/add_cart.svelte';
	import Md from '$lib/comp/marked.svelte';
	import Value from '$lib/item/variation_value.svelte';

	import Status from './_status.svelte';
	import Name from './_name.svelte';
	import Edit_Price from './_price.svelte';
	import Info from './_info.svelte';
	import Variation from './_variation.svelte';
	import Tag from './_tag.svelte';
	import Share from './_share.svelte';

	export let item = {};
	export let edit_mode = false;
	let feedbacks = [];
	let give_feedback = false;
	let mounted = false;

	let open_info = true && item.info;
	let open_feedback = feedbacks && feedbacks.length > 0;
	let open_variation = Object.keys(item.variation).length > 0;
	let open_discount = false;

	const load = async (item_) => {
		feedbacks = [];
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/feedback/${$user.key}/${item_.key}?size=3`
		);
		resp = await resp.json();

		if (resp.status == 200) {
			feedbacks = resp.feedbacks;
			give_feedback = resp.give_feedback;
		}
	};

	onMount(() => {
		mounted = true;
	});

	$: if (mounted) {
		load(item);
	}
</script>

{#if edit_mode}
	<div class="horizontal">
		<span>
			Status: <span
				class="bold"
				style:color={item.status == 'draft'
					? 'var(--cl6)'
					: item.status == 'live'
					? 'var(--cl5)'
					: 'var(--cl4)'}>{item.status}</span
			>
		</span>

		<Button
			class="small round"
			on:click={() => {
				$module = {
					module: Status,
					item
				};
			}}
			tooltip="Edit Status"
		>
			<SVG type="edit" size="12" />
		</Button>
	</div>

	<br />
{/if}

<div class="horizontal">
	<b>{item.name} </b>

	<div class="horizontal">
		<Save {item} />

		{#if edit_mode}
			<Button
				class="small round"
				on:click={() => {
					$module = {
						module: Name,
						item
					};
				}}
				tooltip="Edit Name"
			>
				<SVG type="edit" size="12" />
			</Button>
		{/if}
	</div>
</div>

<div class="horizontal">
	<span class="f2">
		{#each item.tags as tag, i}
			{#if i > 0},{/if}
			<Button
				class="link"
				on:click={() => {
					$loading = true;
					goto(`/shop?${new URLSearchParams({ tag }).toString()}`);
				}}
			>
				{tag}
			</Button>
		{:else}
			No Tag
		{/each}
	</span>

	{#if edit_mode}
		<Button
			class="small round"
			on:click={() => {
				$module = {
					module: Tag,
					item
				};
			}}
			tooltip="Edit tag"
		>
			<SVG type="edit" size="12" />
		</Button>
	{/if}
</div>

<br />

<div class="horizontal">
	<Price {item} />

	<div class="horizontal">
		{#if item.old_price}
			<Button
				class="small round"
				on:click={() => {
					open_discount = !open_discount;
				}}
			>
				<SVG type="info" size="8" />
			</Button>
		{/if}
		{#if edit_mode}
			<Button
				class="small round"
				on:click={() => {
					$module = {
						module: Edit_Price,
						item
					};
				}}
				tooltip="Edit Price"
			>
				<SVG type="edit" size="12" />
			</Button>
		{/if}
	</div>
</div>
{#if item.old_price && open_discount}
	<div transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}>
		<Discount {item} />
	</div>
{/if}

<br />

<div class="horizontal bold">
	Details
	<div class="horizontal">
		<ButtonFold
			open={open_info}
			on:click={() => {
				open_info = !open_info;
			}}
		/>
		{#if edit_mode}
			<Button
				class="small round"
				on:click={() => {
					$module = {
						module: Info,
						item
					};
				}}
				tooltip="Edit Details"
			>
				<SVG type="edit" size="12" />
			</Button>
		{/if}
	</div>
</div>
{#if open_info}
	<div class="f2" transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}>
		{#if item.info}
			<Md md={item.info} />
		{:else}
			No information
		{/if}
	</div>
{/if}

<br />

{#if edit_mode || Object.keys(item.variation).length > 0}
	<div class="horizontal bold">
		Variation{Object.keys(item.variation).length > 1 ? 's' : ''}
		<div class="horizontal">
			<ButtonFold
				open={open_variation}
				on:click={() => {
					open_variation = !open_variation;
				}}
			/>
			{#if edit_mode}
				<Button
					class="small round"
					on:click={() => {
						$module = {
							module: Variation,
							item
						};
					}}
					tooltip="Edit Variation"
				>
					<SVG type="edit" size="12" />
				</Button>
			{/if}
		</div>
	</div>
	{#if open_variation}
		<div class="f2" transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}>
			{#each Object.entries(item.variation) as [key, values]}
				{@const s = values.length > 0 ? 's' : ''}
				<div class="property">
					<span class="bold">{key}{s}: &nbsp;</span>

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

<br />

<div class="horizontal">
	<div class="horizontal">
		<span class="bold">
			Customer{feedbacks.length > 1 ? 's' : ''} Feedback
		</span>
		<Rating rating={item.rating} />
	</div>

	<ButtonFold
		open={open_feedback}
		on:click={() => {
			open_feedback = !open_feedback;
		}}
	/>
</div>

{#if open_feedback}
	<div transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}>
		{#each feedbacks as feedback}
			<Review {feedback} {item} />
		{:else}
			<span class="f2">
				There is no feedback yet.
				<br />
				Only
				{#if !$user.login}
					logged in
				{/if}

				customers who have purchased this item can add a review.
			</span>
			<br />
		{/each}

		{#if give_feedback || feedbacks.length > 0}
			<br />
		{/if}
		{#if give_feedback}
			<Button class="link" href="/{item.slug}/feedback?add=true">Add Review</Button>
		{/if}
		{#if give_feedback && feedbacks.length > 0}
			&nbsp; &nbsp;
		{/if}
		{#if feedbacks.length > 0}
			<Button href="/{item.slug}/feedback" class="link">
				View all
				<SVG type="arrow_right" size="16" />
			</Button>
		{/if}
	</div>
	<br />
{/if}

<div class="floater">
	<div class="horizontal">
		<div class="horizontal">
			<Add_Cart {item} />
			<Button
				href="https://api.whatsapp.com/send?phone=+2348067397793&text=Hi%0AI want to make enquiry concerning ${item.name} on Meji.ng%20{$page
					.url.href}"
				target="_blank"
			>
				<SVG type="whatsapp" />
				Chat
			</Button>
		</div>
		<Button
			class="round"
			on:click={() => {
				$module = {
					module: Share,
					item
				};
			}}
		>
			<SVG type="share" />
		</Button>
	</div>
</div>

<style>
	.horizontal {
		display: flex;
		justify-content: space-between;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.bold {
		font-weight: 500;
		text-transform: capitalize;
	}
	.f2 {
		color: var(--ac2);
	}

	.floater {
		position: sticky;
		bottom: var(--headerHeight);

		padding: var(--sp2) 0;
		margin-top: var(--sp2);
		border-top: 2px solid var(--ac4);

		background-color: var(--ac5);
	}

	@media screen and (min-width: 800px) {
		.floater {
			bottom: var(--sp1);
		}
	}

	.property {
		display: flex;
		flex-wrap: wrap;
	}
	.property:not(:first-child) {
		margin-top: var(--sp1);
	}
</style>
