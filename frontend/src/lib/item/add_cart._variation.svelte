<script>
	import { module, user, toast, loading, state } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import Number from '$lib/number.svelte';
	import Value from '$lib/item/variation_value.svelte';
	import SVG from '$lib/svg.svelte';
	import IG from '$lib/input_group.svelte';

	let item = { ...$module.item };
	let { variation } = item;

	let vars_ = {};
	let quantity = 1;
	let error = {};

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

		let key = `${item.key}_${JSON.stringify(vars_)}`;
		if (!$user.cart.includes(key)) {
			$user.cart.push(key);
			$user = $user;
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				key: item.key,
				variation: vars_,
				quantity,
				ops: 'add'
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$user.cart = resp.user.cart;

			$module = '';
			$toast = {
				status: 200,
				message: `${item.name} added to cart`
			};

			let i = $state.findIndex((x) => x.name == 'cart');
			if (i != -1) {
				$state[i].loaded = false;
			}
		} else {
			$toast = {
				status: 400,
				message: resp.error
			};
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Select variation</b>
	</svelte:fragment>

	{#each Object.entries(variation) as [key, values]}
		<IG name={key} {error}>
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
		</IG>
	{/each}

	<IG name="quantity" {error} let:id>
		<Number bind:value={quantity} {id} />
	</IG>

	<br />

	<Button
		class="primary"
		on:click={() => {
			validate();
		}}
	>
		<SVG type="cart_add" size="18" />
		Add to cart
	</Button>
</Form>

<style>
	.value_row {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
	}
</style>
