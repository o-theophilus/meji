<script>
	import { module, user, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { onMount } from 'svelte';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';
	import Quantity from './quantity.svelte';
	import Value from './variation_value.svelte';

	let { item } = $module;
	let { variation } = item;

	let error = {};
	let vars_ = {};
	let quantity = 1;

	const validate = () => {
		error = {};

		for (let i of Object.keys(variation)) {
			if (!vars_[i]) {
				error[i] = `Please select a ${i}`;
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				key: item.key,
				quantity,
				variation: vars_,
				ops: 'add'
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$user = resp.user;
			$module = '';
		} else {
			error = resp;
		}
	};

	const style = (bgc) => {
		helper.style.backgroundColor = bgc;
		bgc = window.getComputedStyle(helper).backgroundColor;
		const rgb_array = bgc.match(/\d+/g).map(Number);

		const luminance_color = (rgb_array[0] * 299 + rgb_array[1] * 587 + rgb_array[2] * 114) / 1000;
		const luminance_black = (0 * 299 + 0 * 587 + 0 * 114) / 1000;
		const luminance_white = (255 * 299 + 255 * 587 + 255 * 114) / 1000;
		const contrast1 = Math.abs(luminance_color - luminance_black);
		const contrast2 = Math.abs(luminance_color - luminance_white);

		let color = contrast1 > contrast2 ? 'black' : 'white';
		return color;
	};

	let helper;
	let ready = false;
	onMount(() => {
		ready = true;
	});
</script>

<div bind:this={helper} />

<Form>
	<svelte:fragment slot="title">
		<b>Select variation</b>
	</svelte:fragment>

	{#each Object.entries(variation) as [key, values]}
		{#if values.length > 1 && ready}
			<div class="property">
				<span class="bold">{key}</span>

				<div class="value_row">
					{#each values as value}
						<Value
							button
							active={vars_[key] == value}
							{value}
							on:click={() => {
								vars_[key] = value;
							}}
						/>
					{/each}
				</div>

				{#if error[key]}
					<p class="error">
						{error[key]}
					</p>
				{/if}
			</div>
			<br />
		{/if}
	{/each}

	<div class="property">
		<span class="bold"> quantity </span>
		<Quantity
			quantity={1}
			on:done={(e) => {
				quantity = e.detail.quantity || 1;
			}}
		/>

		{#if error.quantity}
			<p class="error">
				{error.quantity}
			</p>
		{/if}
	</div>
	{#if error.error}
		<p class="error">
			{error.error}
		</p>
	{/if}

	<br />

	<Button
		class="primary"
		icon="cart_add"
		name="Add to cart"
		on:click={() => {
			validate();
		}}
	/>
</Form>

<style>
	.property {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);

		color: var(--ac1);
	}

	.bold {
		font-weight: 500;
		text-transform: capitalize;
	}

	.value_row {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);

		color: var(--ac2);
	}
</style>
