<script>
	import { currency, user, module, tick, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Card from '$lib/card.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/button.svelte';

	import Info from '$lib/module/info.svelte';

	import Email from './_email_template.svelte';
	let email;

	export let order;
	let error;

	$: {
		order;
		error = '';
	}

	$: pay = order.info.total_items + order.info.delivery_fee - order.info.account;

	$: config = {
		key: 'pk_test_e349e05c5161ce3ef207ba58a93e40bde8e582fa',
		email: $user?.email,
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
						icon: 'ok'
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
		error = '';
		if (!complete_address) {
			error = 'kindly fill the Shipping Information form';
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
		let mail_content = email.innerHTML;
		error = '';

		$loading = true;

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/${order.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ reference, mail_content })
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
				error = resp.message;
			}
		}
	};
</script>

<svelte:head>
	<script src="https://js.paystack.co/v2/inline.js"></script>
</svelte:head>

<Card>
	<Body>
		<div class="horizontal">
			<Button
				class={complete_address ? 'primary' : ''}
				name="Place Order {pay > 0 ? `(Pay ${currency(pay)})` : ''}"
				on:click={() => {
					validate();
				}}
			/>
		</div>
		{#if error}
			<p class="error">
				{error}
			</p>
		{/if}
		<p class="terms">
			by clicking the order button, you have accepred our <a href="/terms">terms and conditions</a>
		</p>
	</Body>
</Card>

<div bind:this={email} style="display: none;">
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
</style>
