<script>
	import { user, module, tick, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/module/info.svelte';
	import Email from './action.email_template.svelte';
	let email_template;

	export let order;
	let error = {};

	$: {
		order;
		error = {};
	}

	$: pay = order.info.total_items + order.info.delivery_fee - order.info.account;

	$: config = {
		key: import.meta.env.VITE_PAYSTACK_KEY,
		email: $user.email,
		// currency: 'NGN',
		amount: pay * 100,
		onSuccess: (resp) => {
			submit(resp.reference);
		},
		onCancel: () => {
			$module = {
				module: Info,
				status: 400,
				title: 'Payment Canceled',
				message: `The payment process was canceled`,
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
						}
					}
				]
			};
		}
	};

	$: complete_address =
		order.recipient.name &&
		order.recipient.phone &&
		order.recipient.address.line &&
		order.recipient.address.state &&
		order.recipient.address.country &&
		order.recipient.address.local_area &&
		order.recipient.address.postal_code;

	const validate = () => {
		error = {};
		if (!complete_address) {
			error.error = 'kindly fill the Shipping Information form';
		}

		Object.keys(error).length === 0 && place_order();
	};

	const place_order = async () => {
		if (pay > 0) {
			const paystack = new PaystackPop();
			paystack.newTransaction(config);
		} else {
			submit();
		}
	};

	const submit = async (reference = '') => {
		error = {};

		$loading = true;
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/${order.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				reference,
				email_template: email_template.innerHTML.replace(/&amp;/g, '&')
			})
		});

		if (_resp.ok) {
			let resp = await _resp.json();
			$loading = false;

			if (resp.status == 200) {
				$user.acc_balance = resp.data.user.acc_balance;
				tick(resp.data.order);

				$module = {
					module: Info,
					status: 200,
					title: 'Successful',
					message: `Your order was placed succcessfully`,
					button: [
						{
							name: 'Ok',
							icon: 'ok'
						}
					]
				};
			} else {
				error = resp;
			}
		}
	};
</script>

<svelte:head>
	<script src="https://js.paystack.co/v2/inline.js"></script>
</svelte:head>

<div class="horizontal">
	<Button
		class={complete_address ? 'primary' : ''}
		name="Place Order {pay > 0 ? `(Pay ₦${pay.toLocaleString()})` : ''}"
		on:click={() => {
			validate();
		}}
	/>
</div>
<br />
{#if error.error}
	<p class="error">
		{error.error}
	</p>
	<br />
{/if}

<p class="terms">
	by clicking the order button, you have accepred our
	<a href="/terms">terms and conditions</a>
</p>

<div bind:this={email_template} style="display: none;">
	<Email {order} user={$user} />
</div>

<style>
	.horizontal {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.terms {
		font-size: small;
	}
	a {
		color: var(--cl1);
		text-decoration: none;
		font-weight: 500;
	}
	a:hover {
		color: var(--cl2);
	}
</style>
