<script>
	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';

	let item = { ...$module.item };
	if (!['true', 'false'].includes(item.show_discount)) {
		item.discount_date = item.show_discount;
		item.show_discount = 'date';
	}
	let error = {};

	const validate = async () => {
		error = {};

		if (item.price && (!Number.isFinite(item.price) || item.price < 0)) {
			error.price = 'please enter a valid price';
		}

		if (item.show_discount) {
			if (!['true', 'false', 'date'].includes(item.show_discount)) {
				error.show_discount = 'This field is required';
			} else if (item.show_discount == 'date' && !item.discount_date) {
				error.discount_date = 'This field is required';
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				price: item.price,
				show_discount: item.show_discount != 'date' ? item.show_discount : item.discount_date
			})
		});
		resp = await resp.json();
		$loading = false;
		if (resp.status == 200) {
			$portal = {
				type: 'item',
				data: resp.item
			};
			$module = '';
			$toast = {
				status: 200,
				message: 'Price changed'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Edit Price</b>
	</svelte:fragment>

	<IG name="price" {error} bind:value={item.price} type="number" placeholder="Price here" />

	<div class="space">
		Show Discount
		{#if error.show_discount}
			<p class="error">
				{error.show_discount}
			</p>
		{/if}
		<label>
			<input type="radio" bind:group={item.show_discount} value="true" /> Always
		</label>
		<label>
			<input type="radio" bind:group={item.show_discount} value="false" /> Never
		</label>
		<label>
			<input type="radio" bind:group={item.show_discount} value="date" /> Till Date
		</label>
	</div>

	<IG
		name="discount_date"
		label=" "
		{error}
		bind:value={item.discount_date}
		type="datetime"
		placeholder="date here"
		disabled={item.show_discount != 'date'}
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="primary" on:click={validate}>Save</Button>
</Form>

<style>
	.space {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);
	}
</style>
