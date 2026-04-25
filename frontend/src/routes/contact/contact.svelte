<script>
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
</script>

<div class="container">
	<div class="contact">
		<div class="icon">
			<Icon icon="headset" size="24"></Icon>
		</div>

		<div class="ab">
			<div class="a">
				<div class="title">Need more help?</div>
				<div class="copy">Our support team is here for you.</div>
			</div>
			<div class="b">
				<Button
					--button-background-color="var(--cl3)"
					--button-background-color-hover="var(--cl3_)"
					--button-color="white"
					--button-outline-color="transparent"
					icon2="send-horizontal"
					href="/contact"
				>
					Contact Support
				</Button>
			</div>
		</div>
	</div>
</div>

<style>
	.container {
		container-type: inline-size;
	}
	.contact {
		display: flex;
		flex-direction: column;
		gap: 16px;
		align-items: center;

		background-color: var(--bg2);
		margin-top: 52px;
		padding: 40px;
		border-radius: 8px;
		text-align: center;

		.ab {
			display: flex;
			flex-direction: column;
			align-items: center;
			gap: 16px;
			width: 100%;
		}

		.icon {
			display: flex;
			justify-content: center;
			align-items: center;
			color: var(--ft2);
			fill: currentColor;

			width: 48px;
			aspect-ratio: 1;
			flex-shrink: 0;
			border-radius: 40%;
			background-color: var(--bg1);
		}

		.a {
			width: 100%;
		}
		.b {
			flex-shrink: 0;
		}
		.title {
			font-size: 1.2rem;
			font-weight: 800;
			color: var(--ft1);
		}

		.copy {
			font-size: 0.8rem;
		}

		@container (min-width: 400px) {
			.ab {
				flex-direction: column;
				align-items: flex-start;
			}
			flex-direction: row;
			align-items: flex-start;
			text-align: left;
		}

		@container (min-width: 500px) {
			.ab {
				flex-direction: row;
			}
		}
	}
</style>
