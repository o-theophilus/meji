<script>
	import { slide } from 'svelte/transition';
	import { elasticInOut } from 'svelte/easing';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { user, module, loading } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import Button_Fold from '$lib/button_fold.svelte';
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

	$: if ($user) {
		item.save = false;
		for (const i in $user.saves) {
			if ($user.saves[i].key == item.key) {
				item.save = true;
				break;
			}
		}
	}

	let rating = 0;
	if (item.feedbacks) {
		for (let i in item.feedbacks) {
			rating += item.feedbacks[i].rating;
		}
		rating /= item.feedbacks.length;
	}

	export let edit_mode = false;
	let open_info = true && item.info;
	let open_feedback = item.feedbacks && item.feedbacks.length > 0;
	let open_variation = Object.keys(item.variation).length > 0;
	let open_discount = false;
	let review_lenght = 3;
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
			class="tiny"
			icon="edit"
			icon_size="12"
			on:click={() => {
				$module = {
					module: Status,
					item
				};
			}}
			tooltip="Edit Status"
		/>
	</div>

	<br />
{/if}

<div class="horizontal">
	<b>{item.name} </b>

	<div class="horizontal">
		<Save {item} />

		{#if edit_mode}
			<Button
				icon="edit"
				class="tiny"
				icon_size="12"
				on:click={() => {
					$module = {
						module: Name,
						item
					};
				}}
				tooltip="Edit Name"
			/>
		{/if}
	</div>
</div>

<div class="horizontal">
	<span class="f2">
		{#each item.tags as tag, i}
			{#if i > 0},{/if}
			<Button
				name={tag}
				class="link"
				on:click={() => {
					$loading = true;
					// $module = '';
					goto(`/shop?${new URLSearchParams(`tag=${tag}`).toString()}`);
				}}
			/>
		{:else}
			No Tag
		{/each}
	</span>

	{#if edit_mode}
		<Button
			icon="edit"
			icon_size="12"
			class="tiny"
			on:click={() => {
				$module = {
					module: Tag,
					item
				};
			}}
			tooltip="Edit tag"
		/>
	{/if}
</div>

<br />

<div class="horizontal">
	<Price {item} />

	<div class="horizontal">
		{#if item.old_price}
			<Button
				icon="info"
				class="tiny"
				icon_size="8"
				on:click={() => {
					open_discount = !open_discount;
				}}
			/>
		{/if}
		{#if edit_mode}
			<Button
				icon="edit"
				icon_size="12"
				class="tiny"
				on:click={() => {
					$module = {
						module: Edit_Price,
						item
					};
				}}
				tooltip="Edit Price"
			/>
		{/if}
	</div>
</div>
{#if item.old_price && open_discount}
	<div transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}>
		<Discount {item} />
	</div>
{/if}

{#if item.feedbacks && item.feedbacks.length > 0}
	<br />
	<div class="rating">
		<Rating {rating} />
		<div>
			{item.feedbacks.length} rating{#if item.feedbacks.length > 1}s{/if}
		</div>
	</div>
{/if}

<br />

<div class="horizontal bold">
	Details
	<div class="horizontal">
		<Button_Fold
			open={open_info}
			on:click={() => {
				open_info = !open_info;
			}}
		/>
		{#if edit_mode}
			<Button
				icon="edit"
				icon_size="12"
				class="tiny"
				on:click={() => {
					$module = {
						module: Info,
						item
					};
				}}
				tooltip="Edit Details"
			/>
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
			<Button_Fold
				open={open_variation}
				on:click={() => {
					open_variation = !open_variation;
				}}
			/>
			{#if edit_mode}
				<Button
					icon="edit"
					class="tiny"
					icon_size="12"
					on:click={() => {
						$module = {
							module: Variation,
							item
						};
					}}
					tooltip="Edit Variation"
				/>
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
				No Vaiation
			{/each}
		</div>
	{/if}
{/if}

<br />

<div class="horizontal bold">
	Customer{item.feedbacks.length > 1 ? 's' : ''} Feedback

	<Button_Fold
		open={open_feedback}
		on:click={() => {
			open_feedback = !open_feedback;
		}}
	/>
</div>

{#if open_feedback}
	<div transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}>
		{#if item.feedbacks.length > 0}
			<span class="title"> Rating </span>
			<Rating feedback={item.feedbacks} />
			<span class="title"> Reviews </span>

			{#each item.feedbacks.slice(0, review_lenght) as feedback (feedback.id)}
				<Review {feedback} />
			{/each}

			{#if item.feedbacks.length > review_lenght}
				<Button
					name="View all ({item.feedbacks.length})"
					class="tertiary"
					on:click={() => {
						goto(`/${item.id}/feedback`);
					}}
				/>
			{/if}
		{:else}
			<span class="f2">
				There is no feedback yet.
				<br />
				Only
				{#if !$user.login}
					logged in
				{/if}

				customers who have purchased this item may leave a review.
			</span>
		{/if}
	</div>
	<br />
{/if}

<div class="floater">
	<div class="horizontal">
		<div class="horizontal">
			<Add_Cart {item} />
			<Button
				name="Chat"
				icon="whatsapp"
				href="https://api.whatsapp.com/send?phone=+2348067397793&text=Hi%0AI want to make enquiry concerning ${item.name} on Meji.ng%20{$page
					.url.href}"
				target="_blank"
			/>
		</div>
		<Button
			icon="share"
			on:click={() => {
				$module = {
					module: Share,
					item
				};
			}}
		/>
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

	.rating {
		display: flex;
		align-items: center;

		gap: var(--sp1);

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
