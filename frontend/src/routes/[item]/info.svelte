<script>
	import { user, module } from '$lib/store.js';
	import { slide } from 'svelte/transition';
	import { elasticInOut } from 'svelte/easing';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import Button from '$lib/button.svelte';
	import Price from './info.price.svelte';
	import Rating from '$lib/item/rating.svelte';
	import Add_Cart from '$lib/item/add_cart.svelte';
	import Review from '$lib/comp/feedback_review.svelte';
	import Save from '$lib/item/save.svelte';
	import Md from '$lib/comp/marked.svelte';

	import Status from './_status.svelte';
	import Name from './_name.svelte';
	import Variation from './_variation.svelte';
	import tag from './_tag.svelte';
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
	let review_lenght = 3;
</script>

{#if edit_mode}
	<div class="h">
		Status: {item.status}

		<Button
			icon="edit"
			class="tiny"
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

<div class="name h">
	{item.name}

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
			tooltip="Edit Details"
		/>

		<Button
			icon="logo"
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

	<div class="save">
		<Save {item} />
	</div>
</div>

<br />

{#if item.tags.length > 0 || edit_mode}
	<div class="tags">
		{#each item.tags as tag, i}
			{#if i > 0},{/if}
			{tag}
			<!-- <Button
				name={tag}
				class="tag"
				on:click={() => {
					// $state['shop'].search = '';
					// $state['shop'].tag = tag;
					// $state['shop'].page_no = 1;
					// goto('/shop');
				}}
			/> -->
		{/each}
		{#if edit_mode}
			<Button
				icon="edit"
				icon_size="12"
				class="tiny"
				on:click={() => {
					$module = {
						module: tag,
						data: {
							item
						}
					};
				}}
				tooltip="Edit Item tag"
			/>
		{/if}
	</div>
{/if}

<br />
<Price {item} />

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
<div class="title">
	Details
	<Button
		open={open_info}
		on:click={() => {
			open_info = !open_info;
		}}
	/>
</div>
{#if open_info}
	<div transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}>
		{#if item.info}
			<Md md={item.info} />
		{:else}
			No information
		{/if}
	</div>
	<br />
{/if}

<br />

<div class="title">
	Customer{item.feedbacks.length > 1 ? 's' : ''} Feedback

	<Button
		open={open_feedback}
		on:click={() => {
			open_feedback = !open_feedback;
		}}
	/>
</div>

{#if open_feedback}
	<div transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}>
		{#if item.feedbacks && item.feedbacks.length > 0}
			<span class="title"> Rating </span>
			<Rating feedback={item.feedbacks} />
			<span class="title"> Reviews </span>

			{#each item.feedbacks.slice(0, review_lenght) as feedback (feedback.id)}
				<Review {feedback} />
			{/each}

			{#if item.feedbacks.length > review_lenght}
				<!-- <HR /> -->
				<Button
					name="View all ({item.feedbacks.length})"
					class="tertiary"
					on:click={() => {
						goto(`/${item.id}/feedback`);
					}}
				/>
			{/if}
		{:else}
			There is no feedback yet.
			<br />
			<br />
			Only logged in customers who have purchased this item may leave a review.
		{/if}
	</div>
	<br />
{/if}

<div class="floater">
	<div class="h space">
		<div class="h">
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
	.name {
		position: relative;
		font-weight: 500;
	}

	.save {
		position: absolute;
		right: 0;
		top: 0;
	}

	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--sp1);
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
</style>
