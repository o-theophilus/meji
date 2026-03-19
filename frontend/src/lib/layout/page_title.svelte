<script>
	let { title, copy } = $props();
</script>

<section>
	<div class="block">
		<div class="title">
			{@render title?.()}
		</div>
		<div class="copy">
			{@render copy?.()}
		</div>
	</div>
</section>

<style>
	section {
		background-color: var(--title-background-color, var(--bg1));
	}
	.block {
		max-width: var(--title-width, var(--mobileWidth));
		width: 100%;
		margin: auto;
		padding-left: 16px;
		padding-right: 16px;
		padding-top: var(--title-padding-top, 80px);
		padding-bottom: var(--title-padding-bottom, 80px);
		text-align: center;

		@media screen and (min-width: 580px) {
			& {
				padding-left: 24px;
				padding-right: 24px;
			}
		}
	}

	.title {
		font-size: 2rem;
		font-weight: 800;
		color: var(--ft1);
	}
</style>
